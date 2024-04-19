"""Calculates CT & T side likeliehood of winning a round at any given point"""

from typing import List, Dict, Union
import pandas as pd 

from awpy import Demo


def process_tick_data(tick_data: pd.DataFrame, demo: Demo) -> Dict[str, Union[int, str, bool]]:
    """
    Processes individual tick data to extract game state features.

    Args:
        tick_data (pd.DataFrame): DataFrame containing all entries for a single tick.
        demo (Demo): A parsed demo object containing CS2 match data.

    Returns:
        Dict[str, Union[int, str, bool]]: Dictionary containing the game state features for the tick.
    """
    round_number = tick_data['round'].iloc[0]
    map_name = demo.header.map_name
    bomb_planted = tick_data['is_bomb_planted'].iloc[0]
    players_alive_ct = tick_data[(tick_data['side'] == 'CT') & (tick_data['health'] > 0)]['steamid'].nunique()
    players_alive_t = tick_data[(tick_data['side'] == 'TERRORIST') & (tick_data['health'] > 0)]['steamid'].nunique()
    equipment_value_ct = tick_data[(tick_data['side'] == 'CT') & (tick_data['health'] > 0)]['current_equip_value'].sum()
    equipment_value_t = tick_data[(tick_data['side'] == 'TERRORIST') & (tick_data['health'] > 0)]['current_equip_value'].sum()
    hp_remaining_ct = tick_data[(tick_data['side'] == 'CT') & (tick_data['health'] > 0)]['health'].sum()
    hp_remaining_t = tick_data[(tick_data['side'] == 'TERRORIST') & (tick_data['health'] > 0)]['health'].sum()
    
    return {
        "tick": tick_data['tick'].iloc[0],
        "round": round_number,
        "map_name": map_name,
        "bomb_planted": bomb_planted,
        "players_alive_ct": players_alive_ct,
        "players_alive_t": players_alive_t,
        "equipment_value_ct": equipment_value_ct,
        "equipment_value_t": equipment_value_t,
        "hp_remaining_ct": hp_remaining_ct,
        "hp_remaining_t": hp_remaining_t,
    }

def build_feature_matrix(demo: Demo, ticks: Union[int, List[int]]) -> List[Dict[str, Union[int, str, bool]]]:
    """
    Builds the game state feature matrix for specified ticks using a more efficient pandas apply method.

    Args:
        demo (Demo): A parsed demo object containing CS2 match data.
        ticks (Union[int, List[int]]): A single tick or a list of ticks at which to calculate features.

    Returns:
        List[Dict[str, Union[int, str, bool]]]: A list of dictionaries where each dictionary contains the game state features at a given tick.
    
    Raises:
        ValueError: If specified ticks are not found within the demo object.
    """
    if demo.ticks.empty:
        raise ValueError("Demo object does not contain tick data.")

    if isinstance(ticks, int):
        ticks = [ticks]

    # Filtering ticks data for the specified ticks
    filtered_ticks = demo.ticks[demo.ticks["tick"].isin(ticks)]

    if filtered_ticks.empty:
        raise ValueError("No data found for specified ticks.")

    # Applying the external function to each group of tick data
    game_state = filtered_ticks.groupby('tick').apply(lambda x: process_tick_data(x, demo)).tolist()
    return game_state
    

def win_probability(demo: Demo, ticks: Union[int, List[int]]) -> List[Dict[str, float]]:
    """
    Calculate win probabilities for specified ticks in a CS2 match demo.

    Args:
        demo (Demo): A parsed demo object containing CS2 match data.
        ticks (Union[int, List[int]]): A single tick or a list of ticks at which to calculate win probabilities.

    Returns:
        List[Dict[str, float]]: A list of dictionaries with the calculated win probabilities for CT and T sides for each tick.

    Raises:
        NotImplementedError: This function has not yet been implemented.
    """
    raise NotImplementedError("This functionality is not yet implemented.")

