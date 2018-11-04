import pandas as pd

def add_cocktail(cocktail: str, ratios: dict) -> pd.DataFrame:
    df = pd.read_pickle('CocktailsDataFrame.pkl')
    ratio_sum = sum([ratio for ratio in ratios.values()])
    percentages = {drink: round(ratio/ratio_sum,2) for drink, ratio in ratios.items()}
    row = [{'Cocktail': cocktail, 'Ratios': ratios, 'Percentages': percentages}]
    temp_df = pd.DataFrame(row).set_index('Cocktail')
    df = df.append(temp_df)
    df.to_pickle('CocktailsDataFrame.pkl')
    return df


def remove_last_cocktail() -> pd.DataFrame:
    df = pd.read_pickle('CocktailsDataFrame.pkl')
    df = df.iloc[:-1]
    df.to_pickle('CocktailsDataFrame.pkl')
    return df


def add_spirit(brand: str, typ: str, strength: float, price: float) -> pd.DataFrame:
    df = pd.read_pickle('AlcoholDataFrame.pkl')
    row = [{'Brand': brand, 'Type': typ, 'Strength (abv %)': strength, 'Price (/litre)': price}]
    temp_df = pd.DataFrame(row).set_index('Brand')
    appended_df =  df.append(temp_df)
    appended_df.to_pickle('AlcoholDataFrame.pkl')
    return appended_df


def remove_last_spirit() -> pd.DataFrame:
    df = pd.read_pickle('AlcoholDataFrame.pkl')
    df = df.iloc[:-1]
    df.to_pickle('AlcoholDataFrame.pkl')
    return df 