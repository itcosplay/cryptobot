from data import all_emoji


def get_beauty_sum(sum):
    sum = str(sum)

    if sum[0] == '-':
        sum = sum[1:]
        sum = int(sum)
        sum = f'{sum:,}'
        sum = sum.replace(',', '.')
        sum = all_emoji['минус'] + sum
        # sum = '-' + sum
    else:
        sum = int(sum)
        sum = f'{sum:,}'
        sum = sum.replace(',', '.')
        sum = all_emoji['плюс'] + sum
        # sum = '+' + sum

    return str(sum)
