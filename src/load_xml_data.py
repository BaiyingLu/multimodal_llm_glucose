import pandas as pd
import xml.etree.ElementTree as ET


def load_ohiot1dm_xml(xml_file_path):
    """
    Load OhioT1DM XML data into separate dataframes.
    
    Parameters:
    -----------
    xml_file_path : str
        Path to the XML file
        
    Returns:
    --------
    dict
        Dictionary containing dataframes for:
        - 'glucose_level': Glucose measurements
        - 'basal': Basal insulin rates
        - 'tempbasal': Temporary basal rates
        - 'bolus': Insulin bolus events
        - 'meal': Meal events
        - 'step': Step count data
    """
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # Initialize lists to store data
    glucose_data = []
    basal_data = []
    tempbasal_data = []
    bolus_data = []
    meal_data = []
    step_data = []
    
    # Extract glucose level data
    glucose_level = root.find('glucose_level')
    if glucose_level is not None:
        for event in glucose_level.findall('event'):
            glucose_data.append({
                'timestamp': event.get('ts'),
                'value': float(event.get('value'))
            })
    
    # Extract basal insulin data
    basal = root.find('basal')
    if basal is not None:
        for event in basal.findall('event'):
            basal_data.append({
                'timestamp': event.get('ts'),
                'value': float(event.get('value'))
            })
    
    # Extract temporary basal data
    temp_basal = root.find('temp_basal')
    if temp_basal is not None:
        for event in temp_basal.findall('event'):
            tempbasal_data.append({
                'ts_begin': event.get('ts_begin'),
                'ts_end': event.get('ts_end'),
                'value': float(event.get('value'))
            })
    
    # Extract bolus data
    bolus = root.find('bolus')
    if bolus is not None:
        for event in bolus.findall('event'):
            bolus_data.append({
                'ts_begin': event.get('ts_begin'),
                'ts_end': event.get('ts_end'),
                'type': event.get('type'),
                'dose': float(event.get('dose')),
                'bwz_carb_input': float(event.get('bwz_carb_input'))
            })
    
    # Extract meal data
    meal = root.find('meal')
    if meal is not None:
        for event in meal.findall('event'):
            meal_data.append({
                'timestamp': event.get('ts'),
                'type': event.get('type'),
                'carbs': float(event.get('carbs'))
            })
    
    # Extract step data (basis_steps)
    basis_steps = root.find('basis_steps')
    if basis_steps is not None:
        for event in basis_steps.findall('event'):
            step_data.append({
                'timestamp': event.get('ts'),
                'value': float(event.get('value'))
            })
    
    # Create dataframes
    df_glucose = pd.DataFrame(glucose_data)
    df_basal = pd.DataFrame(basal_data)
    df_tempbasal = pd.DataFrame(tempbasal_data)
    df_bolus = pd.DataFrame(bolus_data)
    df_meal = pd.DataFrame(meal_data)
    df_step = pd.DataFrame(step_data)
    
    # Convert timestamp columns to datetime
    if not df_glucose.empty:
        df_glucose['timestamp'] = pd.to_datetime(df_glucose['timestamp'], format='%d-%m-%Y %H:%M:%S')
    
    if not df_basal.empty:
        df_basal['timestamp'] = pd.to_datetime(df_basal['timestamp'], format='%d-%m-%Y %H:%M:%S')
    
    if not df_tempbasal.empty:
        df_tempbasal['ts_begin'] = pd.to_datetime(df_tempbasal['ts_begin'], format='%d-%m-%Y %H:%M:%S')
        df_tempbasal['ts_end'] = pd.to_datetime(df_tempbasal['ts_end'], format='%d-%m-%Y %H:%M:%S')
    
    if not df_bolus.empty:
        df_bolus['ts_begin'] = pd.to_datetime(df_bolus['ts_begin'], format='%d-%m-%Y %H:%M:%S')
        df_bolus['ts_end'] = pd.to_datetime(df_bolus['ts_end'], format='%d-%m-%Y %H:%M:%S')
    
    if not df_meal.empty:
        df_meal['timestamp'] = pd.to_datetime(df_meal['timestamp'], format='%d-%m-%Y %H:%M:%S')
    
    if not df_step.empty:
        df_step['timestamp'] = pd.to_datetime(df_step['timestamp'], format='%d-%m-%Y %H:%M:%S')
    
    return {
        'glucose_level': df_glucose,
        'basal': df_basal,
        'tempbasal': df_tempbasal,
        'bolus': df_bolus,
        'meal': df_meal,
        'step': df_step
    }


# Example usage
if __name__ == "__main__":
    # Load the data
    xml_file = "../ohiot1dm/train/559-ws-training.xml"
    dataframes = load_ohiot1dm_xml(xml_file)
    
    # Access individual dataframes
    df_glucose = dataframes['glucose_level']
    df_basal = dataframes['basal']
    df_tempbasal = dataframes['tempbasal']
    df_bolus = dataframes['bolus']
    df_meal = dataframes['meal']
    df_step = dataframes['step']
    
    # Display info about each dataframe
    print("Glucose Level Data:")
    print(df_glucose.head())
    print(f"Shape: {df_glucose.shape}\n")
    
    print("Basal Insulin Data:")
    print(df_basal.head())
    print(f"Shape: {df_basal.shape}\n")
    
    print("Temporary Basal Data:")
    print(df_tempbasal.head())
    print(f"Shape: {df_tempbasal.shape}\n")
    
    print("Bolus Data:")
    print(df_bolus.head())
    print(f"Shape: {df_bolus.shape}\n")
    
    print("Meal Data:")
    print(df_meal.head())
    print(f"Shape: {df_meal.shape}\n")
    
    print("Step Data:")
    print(df_step.head())
    print(f"Shape: {df_step.shape}\n")
