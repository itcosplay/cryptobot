from emoji import emojize


issuing_office = emojize(':office:', use_aliases=True)    
cash_recive = emojize(':chart_with_upwards_trend:', use_aliases=True)
delivery = emojize(':steam_locomotive:', use_aliases=True)
exchange = emojize(':recycle:', use_aliases=True)
cash_in = emojize(':atm:', use_aliases=True)
cash_out = emojize(':credit_card:', use_aliases=True)

in_process = emojize(':hourglass_flowing_sand:', use_aliases=True)
ready_to_give = emojize(':money_with_wings:', use_aliases=True)

emo_snail = emojize(':cyclone:', use_aliases=True)
warning = emojize(':exclamation:', use_aliases=True)
permit_ready = emojize(':ticket:', use_aliases=True)
permit_end = emojize(':white_check_mark:', use_aliases=True)

plus = emojize(':heavy_plus_sign:', use_aliases=True)
minus = emojize(':heavy_minus_sign:', use_aliases=True)

persone = emojize(':bust_in_silhouette:', use_aliases=True)

buy = '🛍'
transfer = '🤽🏼‍♂️'
replenishment = '📈'
other = 'ℹ️'
cashoutatm = '💵'

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

    'квз': warning,
    'нужно заказать': warning,
    'заказан': permit_ready,
    'отработан': permit_end,

    'Покупка': buy,
    'Перевод': transfer,
    'Пополнение': replenishment,
    'Снятие': cashoutatm,
    'Другие': other,
    'плюс': plus,
    'минус': minus,
    'персона': persone
}
