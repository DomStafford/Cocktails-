import pandas as pd
from typing import List
from CocktailDrinkCreator import *

BRANDLESS_DRINKS = ['Lemon juice', 'Lime juice']
NONALCOHOLIC_DRINKS = ['Lemon juice', 'Lime juice', 'Tonic']

def interact():
    service = _service_selection()
    if service == '1':
        cocktails_or_neat = _cocktails_or_neat()
        if cocktails_or_neat == '1':
            cocktails_df = pd.read_pickle('CocktailsDataFrame.pkl')
            available_cocktails = list(cocktails_df.index)
            print('The available cocktails are: ')
            print(available_cocktails)
            availability = _available_cocktails()
            if availability == 'Y':
                cocktail = _cocktail_selection(available_cocktails)
                quantity_drunk = _quantity_drunk()
                available_brands = _find_available_brands(cocktail)
                choices = _brand_selection(available_brands)
                drink_attributes = _get_drink_attributes(cocktail, int(quantity_drunk), choices)
                print(quantity_drunk + 'ml of ' + cocktail + 'has the following attributes: \n',
                      'Cost: £' + str(drink_attributes[0]), '\n',
                      'Strength: ' + str(drink_attributes[1]) + '%ABV \n',
                      '#Units: ' + str(drink_attributes[2]))
            else:
                _create_new_cocktail()
        else:
            spirit = _choose_neat_spirit()
            quantity_drunk = _quantity_drunk()
            drink_attributes = _get_neat_drink_attributes(spirit, int(quantity_drunk))
            print(quantity_drunk + 'ml of ' + spirit + 'has the following attributes: \n',
            'Cost: £' + str(drink_attributes[0]), '\n',
            'Strength: ' + str(drink_attributes[1]) + '%ABV \n',
            '#Units: ' + str(drink_attributes[2]))

    elif service == '2':
        _add_new_spirit()
    elif service == '3':
        _create_new_cocktail()
    elif service == '4':
        print('The available cocktails are listed below.')
        print(*_get_available_cocktails(), sep='\n')
        print('If the one you want is not listed, then return to the start and add it.')
    else:
        print('The available spirits/liqueurs are given below.')
        print(*_get_available_spirits(), sep = '\n')
        print('If the one you want is not listed, then return to the start and add it.')
    another_service = _another_service()
    if another_service == 'Y':
        interact()
    else:
        return


def _get_drink_attributes(cocktail: str, quantity_drunk: int, brands_used: dict) -> [float, float, float]:
    def add_non_alcoholic_things(brands_used: dict) -> dict:
        brands_used['Lemon juice'] = 'Lemon juice'
        brands_used['Lime juice'] = 'Lime juice'
        return brands_used
    spirits_df = pd.read_pickle('AlcoholDataFrame.pkl')
    cocktails_df = pd.read_pickle('CocktailsDataFrame.pkl')
    add_non_alcoholic_things(brands_used)
    try:
        percentages = cocktails_df.loc[cocktail]['Percentages']
        total_strength = sum([percentage * spirits_df.loc[brands_used[spirit]][
            'Strength (abv %)'] for spirit, percentage in percentages.items()])
        total_cost_per_litre = sum([percentage * spirits_df.loc[brands_used[spirit]][
            'Price (/litre)'] for spirit, percentage in percentages.items()])
        cost = total_cost_per_litre * quantity_drunk / 1000
        units = quantity_drunk * (total_strength / 100) / 10
        return round(cost, 2), round(total_strength, 2), round(units, 1)
    except KeyError as e:
        print('This cocktail and/or spirit is not listed. Check the DataFrame, and add what is required.')
        print('The error message was: ', e)


def _request_user_input(request_message: str, valid_responses: List[str], error_message: str) -> str:
    response = input(request_message)
    if response not in valid_responses:
        print(error_message)
        response = None
        while response is None:
            response = input(request_message)
            if response not in valid_responses:
                print(error_message)
                response = None
    return response


def _service_selection() -> str:
    return _request_user_input('Would you like to: \n'
                               '1. Get steam info for a drink \n'
                               '2. Add a new drink (e.g. spirit/liquer)\n'
                               '3. Add a new cocktail \n'
                               '4. See all available cocktails \n'
                               '5. See all available spirits',
                               ['1', '2', '3', '4', '5'],
                               'Please enter 1-5.')


def _cocktails_or_neat() -> str:
    return _request_user_input('And would you like steam info on \n'
                               '1. Cocktail \n'
                               '2. A spirit neat',
                               ['1', '2'],
                               'Please enter 1 or 2.')


def _available_cocktails() -> str:
    return _request_user_input('Is the cocktail desired avaiable? (Y/N)', ['Y', 'N'],
                               'Please enter Y or N.')


def _cocktail_selection(available_cocktails: list) -> str:
    return _request_user_input('Please write the cocktail. It is case sensitive.',
                               available_cocktails,
                               'Not listed. Try again.')


def _quantity_drunk() -> str:
    return _request_user_input('How much did you/will you drink (ml)?',
                               [str(i) for i in range(200)],
                               'It must be an integer and less than 200ml...u alchy')


def _find_available_brands(cocktail: str) -> dict:
    cocktails_df = pd.read_pickle('CocktailsDataFrame.pkl')
    spirits_df = pd.read_pickle('AlcoholDataFrame.pkl')
    constituents = [x for x in  list(cocktails_df.loc[cocktail]['Ratios'].keys()) if x not in BRANDLESS_DRINKS]
    available_brands = {spirit: list(spirits_df[spirits_df['Type'] == spirit].index) for spirit in constituents}
    return available_brands


def _brand_selection(brands: dict) -> dict:
    choices = {}
    for spirit, available_brands in brands.items():
        if len(available_brands) == 1:
            choices[spirit] = available_brands[0]
            continue
        print('The available brands of ' + spirit + ' are: ', available_brands)
        choices[spirit] = _request_user_input('Which brand of ' + spirit + ' would you like?',
                            available_brands,
                            'Make sure you type it correctly - or just copy and paste it.')
    return choices

def _print_message_from_enumeration(enumerated_list: list, print_message = '', post_message = None):
    for el in enumerated_list:
        print_message += str(el[0]) + '. ' + el[1] + ' \n'
    if post_message is None:
        print(print_message[:-2])
    else:
        print_message += post_message
        print(print_message)

def _create_new_cocktail():
    spirits_df = pd.read_pickle('AlcoholDataFrame.pkl')
    list_of_spirits_enumerated =  list(enumerate(spirits_df['Type'].unique()))
    _print_message_from_enumeration(list_of_spirits_enumerated,
                                    'Let\'s add the cocktail now. Choose from the availalbe spirits one at a time. \n '
                                    'The available spirits are: \n',
                                    'Keep on adding until you are done.\n Also, at present, I cba let you add new '
                                    'spirits here too, exit to the beginning if '
                                    'the spirit isn\'t here.')
    stop_requesting = False
    spirits = []
    while not stop_requesting:
        number_selected = _request_user_input('Which number?',
                                      [str(i) for i in range(len(list_of_spirits_enumerated))],
                                      'Must be a number between 0 and ' + str(len(list_of_spirits_enumerated)))
        spirits.append(list_of_spirits_enumerated[int(number_selected)][1])
        stop_question = _request_user_input('Add another?(Y/N)',
                                            ['Y', 'N'],
                                            'Must be Y/N')
        if stop_question == 'N':
            stop_requesting = True
    ratios = {}
    for spirit in spirits:
        ratios[spirit] = float(_request_user_input('How many parts ' + spirit + '?',
                                             [str(i) for i in range(20)],
                                             'Do the rations in reasonable numbers - between 1 to 20'))
    cocktail_name = input('What is it called?')
    add_cocktail(cocktail_name, ratios)


def _choose_neat_spirit() -> str:
    spirits_df = pd.read_pickle('AlcoholDataFrame.pkl')
    enumerated_spirits = list(enumerate(spirits_df[~spirits_df['Type'].isin(NONALCOHOLIC_DRINKS)].index))
    _print_message_from_enumeration(enumerated_spirits,
                                    'The available spirits/liqueurs are: \n', post_message=None)
    choice = _request_user_input('',
                                 [str(i) for i in range(len(enumerated_spirits))],
                                 'Try again.')
    return enumerated_spirits[int(choice)][1]


def _get_neat_drink_attributes(spirit: str, quantity_drunk: int) -> [float, float, float]:
    spirits_df = pd.read_pickle('AlcoholDataFrame.pkl')
    strength = spirits_df.loc[spirit]['Strength (abv %)']
    price_per_litre = spirits_df.loc[spirit]['Price (/litre)']
    units = quantity_drunk * (strength / 100) / 10
    return round(price_per_litre * quantity_drunk / 1000,2), round(strength,2), round(units,1)


def _choose_type() -> str:
    spirits_df = pd.read_pickle('AlcoholDataFrame.pkl')
    available_types = list(enumerate(spirits_df['Type'].unique()))
    _print_message_from_enumeration(available_types,'What kind of spirit is it?\n',
                                    str(len(available_types)) + '. It is not listed.')
    choice = _request_user_input('',
                                 [str(i) for i in range(len(available_types)+1)],
                                 'Enter one of the available numbers.')
    if choice != str(len(available_types)):
        return available_types[int(choice)][1]
    else:
        return input('In that case, please enter the spirit/liqueur here.')


def _add_new_spirit():
    type_of_drink = _choose_type()
    brand = input('What brand is it? E.g. Tanqueray')
    strength = input('What is its strength in percentage form? E.g. 47.3')
    cost = input('How much does it cost per litre?')
    print_message = 'So you are adding a ' + type_of_drink + ' called ' + brand \
                    + ' which is ' + strength + '%(ABV) at £' + cost + '/litre. \n' \
                    + 'Is this correct? (Y/N)'
    correct = _request_user_input(print_message, ['Y', 'N'], 'Try again, must be Y/N.')
    if correct == 'Y':
        add_spirit(brand = brand, typ = type_of_drink,
                   strength =  float(strength), price = float(cost))
    else:
        print('Ok, trying again.')
        _add_new_spirit()


def _get_available_cocktails() -> list:
    cocktails_df = pd.read_pickle('CocktailsDataFrame.pkl')
    return list(cocktails_df.index)

def _get_available_spirits() -> list:
    spirits_df = pd.read_pickle('AlcoholDataFrame.pkl')
    return list(spirits_df[~spirits_df['Type'].isin(NONALCOHOLIC_DRINKS)].index)

def _another_service() -> str:
    return _request_user_input('Another service? (Y/N)',
                               ['Y', 'N'],
                               'Enter Y or N.')