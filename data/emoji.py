from emoji import emojize


issuing_office = emojize(':office:', use_aliases=True)    
cash_recive = emojize(':chart_with_upwards_trend:', use_aliases=True)
delivery = emojize(':steam_locomotive:', use_aliases=True)
exchange = emojize(':recycle:', use_aliases=True)
cash_in = emojize(':atm:', use_aliases=True)
cash_out = emojize(':credit_card:', use_aliases=True)

in_process = emojize(':hourglass_flowing_sand:', use_aliases=True)
ready_to_give = emojize(':money_with_wings:', use_aliases=True)

emo_snail = emojize(':snail:', use_aliases=True)
warning = emojize(':exclamation:', use_aliases=True)

all_emoji = {
    'выдача в офисе': issuing_office,
    'прием кэша': cash_recive,
    'доставка': delivery,
    'обмен': exchange,
    'кэшин': cash_in,
    'снятие с карт': cash_out,

    'В обработке': in_process,
    'Готово к выдаче': ready_to_give,

    'back__main_menu': emo_snail,
    'квз': warning
}