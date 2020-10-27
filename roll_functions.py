import numpy as np 

def check_advantage(dice_sides):
    if dice_sides[-1] == 'a':
        return 1
    if dice_sides[-1] == 'd':
        return -1
    else:
        return 0

def split_input(string):
    return string.split(',')

def comment_criticals(message, fails, hits):
    if fails == 1:
        message += f'. 1 CRITICAL FAILURE'
    if hits == 1:
        message += f'. 1 CRITICAL SUCCESS'
    if fails > 1:
        message += f'. {fails} CRITICAL FAILURES'
    if hits > 1:
        message += f'. {hits} CRITICAL SUCCESSES!'
    return message

def check_if_modifier(dice_input):
    first_character = dice_input.strip()[0]
    if first_character == '+':
        return 1
    if first_character == '-':
        return -1
    if first_character != '+' and first_character != '-':
        return 0

def check_if_dice_modifier(roll_list):
    for i in range(0, len(roll_list)):
        if i != len(roll_list)-1:
            if roll_list[i+1]['is_modifier'] == 1 or roll_list[i+1]['is_modifier'] == -1:
                roll_list[i]['has_dice_modifier'] = True
            else:
                roll_list[i]['has_dice_modifier'] = False
    else:
         roll_list[i]['has_dice_modifier'] = False

def split_roll(input):
    split_1 = input.split('d', 1)
    try:
        dice_count = int(split_1[0].strip())
    except:
        dice_count = 1
    if '+' not in split_1[1] and '-' not in split_1[1]:
        dice_sides = split_1[1].strip()
        advantage = check_advantage(dice_sides)
        if advantage == 0:
            dice_sides = int(dice_sides)
        else:
            dice_sides = int(dice_sides[0:-1])
        modifier = 0
        return dice_count, dice_sides, advantage, modifier
    if '+' in split_1[1]:
        split_2 = split_1[1].split('+')
        modifier = int(split_2[1].strip())
        dice_sides = split_2[0].strip()
        advantage = check_advantage(dice_sides)
        if advantage == 0:
            dice_sides = int(dice_sides)
        else:
            dice_sides = int(dice_sides[0:-1])
        return dice_count, dice_sides, advantage, modifier
    if '-' in split_1[1]:
        split_2 = split_1[1].split('-')
        modifier = 0 - int(split_2[1].strip())
        dice_sides = split_2[0].strip()
        advantage = check_advantage(dice_sides)
        if advantage == 0:
            dice_sides = int(dice_sides)
        else:
            dice_sides = int(dice_sides[0:-1])
        return dice_count, dice_sides, advantage, modifier

def count_criticals(rolls):
    critical_fails = np.count_nonzero(1 == rolls)
    critical_hits = np.count_nonzero(20 == rolls)
    return critical_fails, critical_hits

def roll_dice(dice_count, dice_sides, advantage):
    if advantage == 1 or advantage == -1:
        rolls = []
        for i in range(0, dice_count):
            rolls.append(np.random.randint(1, dice_sides+1, 2))
        fails, hits = 0, 0
        if dice_sides == 20:
            fails, hits = count_criticals(rolls)
        return rolls, fails, hits
    else:
        rolls = np.random.randint(1, dice_sides+1, dice_count)
        fails, hits = 0, 0
        if dice_sides == 20:
            fails, hits = count_criticals(rolls)
        return rolls, fails, hits

def roll_them_dice(user_input_string):
    to_roll = split_input(user_input_string)
    roll_list = []
    roll_number = 0

#get the info for each dice
    for roll in to_roll:
        roll_dict = {}
        roll_dict['is_modifier'] = check_if_modifier(roll)
        if roll_dict['is_modifier'] == 0:
            roll_dict['dice_count'], roll_dict['dice_sides'], roll_dict['advantage'], roll_dict['modifier'] = split_roll(roll)
            roll_dict['roll_number'] = roll_number
            roll_list.append(roll_dict)
            roll_number += 1
        else: 
            roll_dict['dice_count'], roll_dict['dice_sides'], roll_dict['advantage'], roll_dict['modifier'] = split_roll(roll.strip()[1:])
            roll_dict['roll_number'] = roll_number
            roll_list.append(roll_dict)
            roll_number += 1

    for roll in roll_list:
        roll['result'], roll['fails'], roll['hits'] = roll_dice(roll['dice_count'], roll['dice_sides'], roll['advantage'])

    check_if_dice_modifier(roll_list)

    roll_number = 0
# having collected the info for each dice, we now turn these into outputs 

    for roll in roll_list:
# for very simple rolls of a single dice with no modifiers or advantage
        if roll['dice_count'] == 1 and roll['is_modifier'] == 0 and roll['modifier'] == 0 and roll['has_dice_modifier'] == 0 and roll['advantage'] == 0 and roll['dice_sides'] != 20:
            result_string = str((roll['result']))[1:-1]
            message = f' rolled **{result_string}**.'
            roll['message'] = message

# for rolls (like damage rolls) that are not d20 and don't have advantage
        elif roll['dice_sides'] != 20 and roll['is_modifier'] == 0 and roll['advantage'] == 0:
            try:
                if roll['has_dice_modifier']:
                    modifier_2 = roll_list[roll_number+1]['result'].sum() + roll_list[roll_number+1]['modifier']
                    if roll_list[roll_number+1]['is_modifier'] == -1:
                        modifier_2 = -1 * modifier_2
                else:
                    modifier_2 = 0
            except:
                modifier_2 = 0
            total_modifier = roll['modifier'] + modifier_2
            final_roll = roll['result'].sum() + total_modifier
            sum_statement = ''
            modifier_string = ''
            if roll['modifier'] != 0:
                modifier_string = ' + ' + str(roll['modifier'])
            if modifier_2 != 0:
                modifier_string += f' + {str(modifier_2)}'
            for i in range(0, len(roll['result'])):
                if i != len(roll['result'])-1:
                    roll_string = str(roll['result'][i])
                    sum_statement += f'{roll_string} + '
                else:
                    sum_statement += str(roll['result'][i])
            message = f' rolled **{final_roll}**. (({sum_statement}){modifier_string} = {final_roll})'
            fails, hits = count_criticals(roll['result'])
            roll['message'] = message

# for rolls with advantage we will want to see all the rolls + modifiers
        elif roll['dice_sides'] == 20 and roll['advantage'] != 0 and roll['is_modifier'] == 0:
            try:
                if roll['has_dice_modifier']:
                    modifier_2 = roll_list[roll_number+1]['result'].sum() + roll_list[roll_number+1]['modifier']
                    if roll_list[roll_number+1]['is_modifier'] == -1:
                        modifier_2 = -1 * modifier_2
                else:
                    modifier_2 = 0
            except:
                modifier_2 = 0
            total_modifier = roll['modifier'] + modifier_2
            if roll['advantage'] == 1:
                outcomes = [x.max() for x in roll['result']]
            if roll['advantage'] == -1:
                outcomes = [x.min() for x in roll['result']]
            final_outcomes = np.array(outcomes) + total_modifier
            final_outcomes_statement = str(list(final_outcomes))[1:-1].strip().replace('  ', ' ').replace(' ', ' & ')
            final_outcomes_formatted = final_outcomes_statement.replace(' & ', '** & **').replace(',', ' ')
            # make a string for modifiers
            modifier_string = ''
            if roll['modifier'] != 0:
                modifier_string = ' + ' + str(roll['modifier'])
            if modifier_2 != 0:
                modifier_string += f' + {str(modifier_2)}'
            sum_statement = ''
            for i in range(0, len(roll['result'])):
                roll_tuple = roll['result'][i]
                if roll['advantage'] == 1:
                    if i != len(roll['result'])-1:
                        sum_statement += f'({roll_tuple.min()} , **{roll_tuple.max()}**){modifier_string} = {final_outcomes[i]}, '
                    else:
                        sum_statement += f'({roll_tuple.min()} , **{roll_tuple.max()}**){modifier_string} = {final_outcomes[i]}'
                if roll['advantage'] == -1:
                    if i != len(roll['result'])-1:
                        sum_statement += f'(**{roll_tuple.min()}** , {roll_tuple.max()}){modifier_string} = {final_outcomes[i]}, '
                    else:
                        sum_statement += f'(**{roll_tuple.min()}** , {roll_tuple.max()}){modifier_string} = {final_outcomes[i]}'
            message = f' rolled **{final_outcomes_formatted}**. ({sum_statement})'
            fails, hits = count_criticals(np.array(outcomes))
            message = comment_criticals(message, fails, hits)
            roll['message'] = message

# for rolls of d20 that do not have advantage, where we want to see each roll + modifiers
        elif roll['dice_sides'] == 20 and roll['advantage'] == 0 and roll['is_modifier'] == 0:
            try:
                if roll['has_dice_modifier']:
                    modifier_2 = roll_list[roll_number+1]['result'].sum() + roll_list[roll_number+1]['modifier']
                    if roll_list[roll_number+1]['is_modifier'] == -1:
                        modifier_2 = -1 * modifier_2
                else:
                    modifier_2 = 0
            except:
                modifier_2 = 0
            total_modifier = roll['modifier'] + modifier_2
            final_outcomes = np.array(roll['result']) + total_modifier
            final_outcomes_statement = str(final_outcomes)[1:-1].strip().replace('  ', ' ').replace(' ', ' & ')
            final_outcomes_formatted = final_outcomes_statement.replace(' & ', '** & **')
            modifier_string = ''
            if roll['modifier'] != 0:
                modifier_string = ' + ' + str(roll['modifier'])
            if modifier_2 != 0:
                modifier_string += f' + {str(modifier_2)}'
            sum_statement = ''
            if modifier_string != '':
                for i in range(0, len(roll['result'])):
                    result_str = str(roll['result'][i])
                    if i != len(roll['result'])-1:
                        sum_statement += f'({result_str}){modifier_string} = {final_outcomes[i]}, '
                    else:
                        sum_statement += f'({result_str}){modifier_string} = {final_outcomes[i]}'
                sum_statement = f'({sum_statement})'
            message = f' rolled **{final_outcomes_formatted}**. {sum_statement}'
            fails, hits = count_criticals(roll['result'])
            message = comment_criticals(message, fails, hits)
            roll['message'] = message
    roll_number += 1

    return roll_list



