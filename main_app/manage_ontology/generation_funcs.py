
def return_outfit(data):
    if data[-2] == 'chinese_style':
        return 'outfit_000000', data[-1]
    elif data[-2] == 'japanese_style':
        return 'outfit_000001', data[-1]
    elif data[-2] == 'korean_style':
        return 'outfit_000002', data[-1]
    elif data[-2] == 'english_style':
        return 'outfit_000003', data[-1]
    elif data[-2] == 'scandinavian_style':
        return 'outfit_000004', data[-1]
    elif data[-2] == 'computer_games':
        return 'outfit_000005', data[-1]
    elif data[-2] == 'epic_fantasy':
        return 'outfit_000006', data[-1]
    elif data[-2] == 'fairy_tales':
        return 'outfit_000007', data[-1]
