from dataclasses import dataclass, field

from typing import List

import polars as pl

import numpy as np

from kloppy.domain import Dimension, Unit, Orientation

from ...utils import (
    DefaultSettings,
    DefaultDataset,
    AmericanFootballPitchDimensions,
    add_dummy_label_column,
    add_graph_id_column,
)

from .objects import Column, Group, Constant


@dataclass
class BigDataBowlDataset(DefaultDataset):
    def __init__(
        self,
        tracking_file_path: str,
        players_file_path: str,
        plays_file_path: str,
        sample_rate: float = None,
        max_player_speed: float = 12.0,
        max_ball_speed: float = 28.0,
        max_player_acceleration: float = 6.0,
        max_ball_acceleration: float = 13.5,
        orient_ball_owning: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.tracking_file_path = tracking_file_path
        self.players_file_path = players_file_path
        self.plays_file_path = plays_file_path
        self.sample_rate = 1 if sample_rate is None else sample_rate

        self._max_player_speed = max_player_speed
        self._max_ball_speed = max_ball_speed
        self._max_player_acceleration = max_player_acceleration
        self._max_ball_acceleration = max_ball_acceleration
        self._orient_ball_owning = orient_ball_owning

        self.load()

    def __apply_settings(
        self,
    ):
        return DefaultSettings(
            provider="nfl",
            home_team_id=None,
            away_team_id=None,
            pitch_dimensions=AmericanFootballPitchDimensions(),
            orientation=(
                Orientation.BALL_OWNING_TEAM
                if self._orient_ball_owning
                else Orientation.NOT_SET
            ),
            max_player_speed=self._max_player_speed,
            max_ball_speed=self._max_ball_speed,
            max_player_acceleration=self._max_player_acceleration,
            max_ball_acceleration=self._max_ball_acceleration,
            ball_carrier_threshold=None,
        )

    def load(self):
        self.settings = self.__apply_settings()

        pitch_length = self.settings.pitch_dimensions.pitch_length
        pitch_width = self.settings.pitch_dimensions.pitch_width

        sample = 1.0 / self.sample_rate

        df = pl.scan_csv(
            self.tracking_file_path,
            separator=",",
            encoding="utf8",
            null_values=["NA", "NULL", ""],
            try_parse_dates=True,
        )

        play_direction = "left"

        if "club" in df.collect_schema().names():
            df = df.with_columns(pl.col(Column.CLUB).alias(Column.TEAM))
            df = df.drop(Column.CLUB)

        if self._orient_ball_owning:
            df = (
                df.with_columns(
                    pl.when(pl.col("playDirection") == play_direction)
                    .then(pl.col(Column.ORIENTATION) + 180)  # rotate 180 degrees
                    .otherwise(pl.col(Column.ORIENTATION))
                    .alias(Column.ORIENTATION),
                    pl.when(pl.col("playDirection") == play_direction)
                    .then(pl.col(Column.DIRECTION) + 180)  # rotate 180 degrees
                    .otherwise(pl.col(Column.DIRECTION))
                    .alias(Column.DIRECTION),
                )
                .with_columns(
                    [
                        (pl.col(Column.X) - (pitch_length / 2)).alias(Column.X),
                        (pl.col(Column.Y) - (pitch_width / 2)).alias(Column.Y),
                        # convert to radian on (-pi, pi) range
                        (
                            ((pl.col(Column.ORIENTATION) * np.pi / 180) + np.pi)
                            % (2 * np.pi)
                            - np.pi
                        ).alias(Column.ORIENTATION),
                        (
                            ((pl.col(Column.DIRECTION) * np.pi / 180) + np.pi)
                            % (2 * np.pi)
                            - np.pi
                        ).alias(Column.DIRECTION),
                    ]
                )
                .with_columns(
                    [
                        pl.when(pl.col("playDirection") == play_direction)
                        .then(pl.col(Column.X) * -1.0)
                        .otherwise(pl.col(Column.X))
                        .alias(Column.X),
                        pl.when(pl.col("playDirection") == play_direction)
                        .then(pl.col(Column.Y) * -1.0)
                        .otherwise(pl.col(Column.Y))
                        .alias(Column.Y),
                        # set "football" to nflId -9999 for ordering purposes
                        pl.when(pl.col(Column.TEAM) == Constant.BALL)
                        .then(-9999.9)
                        .otherwise(pl.col(Column.OBJECT_ID))
                        .alias(Column.OBJECT_ID),
                    ]
                )
                .with_columns(
                    [
                        pl.lit(play_direction).alias("playDirection"),
                    ]
                )
                .filter((pl.col(Column.FRAME_ID) % sample) == 0)
            ).collect()
        else:
            raise NotImplementedError(
                "Currently, BigDataBowlDataset only allows Orientation.BALL_OWNING"
            )

        players = pl.read_csv(
            self.players_file_path,
            separator=",",
            encoding="utf8",
            null_values=["NA", "NULL", ""],
            schema_overrides={"birthDate": pl.Date},
            ignore_errors=True,
        )
        if "position" in players.columns:
            players = players.with_columns(
                pl.col("position").alias(Column.OFFICIAL_POSITION)
            )
            players = players.drop("position")

        players = players.with_columns(
            pl.col(Column.OBJECT_ID)
            .cast(pl.Float64, strict=False)
            .alias(Column.OBJECT_ID)
        )
        players = self._convert_weight_height_to_metric(df=players)

        plays = pl.read_csv(
            self.plays_file_path,
            separator=",",
            encoding="utf8",
            null_values=["NA", "NULL", ""],
            try_parse_dates=True,
        )

        df = df.join(
            (
                players.select(
                    [
                        Column.OBJECT_ID,
                        Column.OFFICIAL_POSITION,
                        Column.HEIGHT_CM,
                        Column.WEIGHT_KG,
                    ]
                )
            ),
            on=Column.OBJECT_ID,
            how="left",
        )
        df = df.join(
            (plays.select(Group.BY_PLAY_POSSESSION_TEAM)),
            on=[Column.GAME_ID, Column.PLAY_ID],
            how="left",
        )
        self.data = df

        # update pitch dimensions to how it looks after loading
        self.settings.pitch_dimensions = AmericanFootballPitchDimensions(
            x_dim=Dimension(min=-pitch_length / 2, max=pitch_length / 2),
            y_dim=Dimension(min=-pitch_width / 2, max=pitch_width / 2),
            standardized=False,
            unit=Unit.YARDS,
            pitch_length=pitch_length,
            pitch_width=pitch_width,
        )

        return self.data, self.settings

    def add_dummy_labels(
        self, by: List[str] = ["gameId", "playId", "frameId"]
    ) -> pl.DataFrame:
        self.data = add_dummy_label_column(self.data, by, self._label_column)
        return self.data

    def add_graph_ids(self, by: List[str] = ["gameId", "playId"]) -> pl.DataFrame:
        self.data = add_graph_id_column(self.data, by, self._graph_id_column)
        return self.data

    @staticmethod
    def _convert_weight_height_to_metric(df: pl.DataFrame):
        df = df.with_columns(
            [
                pl.col("height")
                .str.extract(r"(\d+)")
                .cast(pl.Float64)
                .alias("feet"),  # Extract feet and cast to float
                pl.col("height")
                .str.extract(r"\d+-(\d+)", 1)
                .cast(pl.Float64)
                .alias("inches"),  # Extract inches and cast to float
            ]
        )
        # Convert height and weight to centimeters and kilograms
        # Round them to 0.1 to make sure we don't leak any player specific info
        df = (
            df.with_columns(
                [
                    ((pl.col("feet") * 30.48 + pl.col("inches") * 2.54) / 10)
                    .round(0)
                    .alias(Column.HEIGHT_CM),
                    ((pl.col("weight") * 0.453592) / 10)
                    .round(0)
                    .alias(Column.WEIGHT_KG),
                ]
            )
            .with_columns(
                [
                    (pl.col(Column.HEIGHT_CM) * 10).alias(Column.HEIGHT_CM),
                    (pl.col(Column.WEIGHT_KG) * 10).alias(Column.WEIGHT_KG),
                ]
            )
            .drop(["height", "feet", "inches", "weight"])
        )
        return df
