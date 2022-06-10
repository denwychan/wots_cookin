

def dietary_tagging(df):
    """function that applies dietary tags to recipes dataframe"""

    #dictionary containing tag words for dietary items
    dietary_req = {
            'Dairy free': {'Cheese', 'Butter', 'Margarine', 'Yogurt', 'Cream', 'Ice cream'},
            'No eggs': {'egg'},
            'Nut free': {'Brazil nut', 'Almond', 'Cashew', 'Macadamia nut', 'Pistachio','Pine nut',
                         'Walnut','peanut'},
            'No shellfish': {'Shrimp','Prawn','Crayfish', 'Lobster', 'Squid', 'Scallops','clam'},
            'Gluten free': {'flour', 'wheat', 'pasta', 'noodle', 'bread', 'crust'},
            'No soy': {'soy', 'tofu', 'soya'},
            'Vegetarian': {'beef','pork','lamb','steak','chicken','fish','tuna','cod','salmon',
                           'duck','meat','ham','anchovies','snapper'},
            'Vegan': {'honey'} 
    }

    def dietary_tags(row, types):
        """function that applies dietary tagging for specific diet group"""
        for item in dietary_req[types]:
            if item.lower() in ' '.join(row).lower():
                    return 1
        return 0

    #iterate through dietary groups and apply tags to each recipe
    for key in dietary_req:
        df[key] = df['Cleaned_Ingredients'].apply(lambda x: dietary_tags(x, types = key))

    #apply tags for vegetarian and vegan requirements
    df['Vegetarian'] = df[['Vegetarian','No shellfish']].max(axis=1)
    df['Vegan'] = df[['Dairy free','No eggs','No shellfish','Vegetarian','Vegan']].max(axis=1)

    return df
