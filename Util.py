import os
import re

def calculate_score(category, dice):
    """주사위와 카테고리에 따른 점수 계산"""
    # 주사위 개수 세기
    counts = [0] * 7  # index 0은 미사용, 1-6은 주사위 값
    total = 0
    
    for digit in dice:
        num = int(digit)
        counts[num] += 1
        total += num
    
    # 기본 카테고리 (1000배)
    if category == 'ONE':
        return counts[1] * 1000
    elif category == 'TWO':
        return counts[2] * 2000
    elif category == 'THREE':
        return counts[3] * 3000
    elif category == 'FOUR':
        return counts[4] * 4000
    elif category == 'FIVE':
        return counts[5] * 5000
    elif category == 'SIX':
        return counts[6] * 6000
    
    # 조합 카테고리
    elif category == 'CHOICE':
        return total * 1000
    elif category == 'FOUR_OF_A_KIND':
        # 4개 이상 같은 숫자가 있는지 확인
        for i in range(1, 7):
            if counts[i] >= 4:
                return total * 1000
        return 0
    elif category == 'FULL_HOUSE':
        # 3개 + 2개 조합 확인
        has_three = any(count == 3 for count in counts[1:])
        has_two = any(count == 2 for count in counts[1:])
        return total * 1000 if (has_three and has_two) else 0
    elif category == 'SMALL_STRAIGHT':
        # 4개 연속 숫자 확인
        dice_set = set(dice)
        if {'1','2','3','4'}.issubset(dice_set) or \
           {'2','3','4','5'}.issubset(dice_set) or \
           {'3','4','5','6'}.issubset(dice_set):
            return 15000
        return 0
    elif category == 'LARGE_STRAIGHT':
        # 5개 연속 숫자 확인
        sorted_dice = ''.join(sorted(dice))
        if sorted_dice == '12345' or sorted_dice == '23456':
            return 30000
        return 0
    elif category == 'YACHT':
        # 모든 주사위가 같은 숫자인지 확인
        return 50000 if len(set(dice)) == 1 else 0
    
    return 0

def parse_yacht_data(game_data, my_team):
    """
    게임 데이터를 파싱해서 내 점수 결과와 배팅 정보를 반환
    my_team: 'FIRST' 또는 'SECOND'
    """
    lines = game_data.strip().split('\n')
    
    my_results = []  # 내가 선택한 카테고리와 점수들
    my_bids = []     # 내 배팅 금액들
    opponent_bids = []  # 상대방 배팅 금액들
    
    for line in lines:
        if line.startswith('PUT'):
            # PUT FIRST* CHOICE* 43634 형태 파싱
            parts = line.split(' ')
            if len(parts) >= 3:
                player = parts[1].strip()  # FIRST 또는 SECOND
                category = parts[2].strip()
                dice = parts[3].strip()
                
                if player == my_team:
                    score = calculate_score(category, dice)
                    my_results.append({
                        'category': category,
                        'dice': dice,
                        'score': score
                    })
        elif line.startswith('BID'):
            # BID FIRST A 460 형태 파싱
            parts = line.split(' ')
            if len(parts) >= 4:
                player = parts[1].strip()  # FIRST 또는 SECOND
                choice = parts[2].strip()  # A 또는 B
                bid_amount = int(parts[3].strip())
                
                if player == my_team:
                    my_bids.append(bid_amount)
                else:
                    opponent_bids.append(bid_amount)
    
    return my_results, my_bids, opponent_bids

def load_game_data_from_file(filename):
    """
    파일에서 게임 데이터를 읽어오기
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"파일 '{filename}'을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return None
    
def print_data(results):
    category = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'CHOICE', 'FOUR_OF_A_KIND', 'FULL_HOUSE', 'SMALL_STRAIGHT', 'LARGE_STRAIGHT', 'YACHT']
    target_categories = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']
    bonus_sum = sum(item['score'] for item in results if item['category'] in target_categories)
    sorted_data = sorted(results, key=lambda item: category.index(item['category']))
    
    bonus = 0
    if (bonus_sum >= 63000):
        bonus = 35000
    s = 0

    for data in sorted_data:
        print(f"{data['category']} : {data['score']} ({data['dice']})")
        s += data['score']
        if (data['category'] == 'SIX'):
            print(f"BONUS : {bonus} ({bonus_sum})")
    print(f"TOTAL : {s + bonus}")

def print_bid_analysis(my_bids, opponent_bids):
    """배팅 분석 결과 출력"""
    if my_bids:
        my_avg = sum(my_bids) / len(my_bids)
        my_total = sum(my_bids)
        print(f"내 배팅 평균: {my_avg:.1f} (총 {len(my_bids)}회, 총액 {my_total})")
    
    if opponent_bids:
        opp_avg = sum(opponent_bids) / len(opponent_bids)
        opp_total = sum(opponent_bids)
        print(f"상대 배팅 평균: {opp_avg:.1f} (총 {len(opponent_bids)}회, 총액 {opp_total})")
    
def read_files(directory_path):
    files = []
    if os.path.exists(directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                files.append(item_path)
    return files

def calculate_average(total_result):
    category = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'CHOICE', 'FOUR_OF_A_KIND', 'FULL_HOUSE', 'SMALL_STRAIGHT', 'LARGE_STRAIGHT', 'YACHT']
    target_categories = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']

    avg = {}
    avg['BONUS'] = 0
    
    s = 0
    mx = 0
    mn = 300000
    
    for result in total_result:
        total = 0
        for data in result:
            
            if data['category'] not in avg:
                avg[data['category']] = 0
            
            if data['category'] in ['SMALL_STRAIGHT', 'LARGE_STRAIGHT', 'YACHT']:
                avg[data['category']] += 1 if data['score'] > 0 else 0
            else:
                avg[data['category']] += data['score']
            
            total += data['score']
            
        bonus_sum = sum(item['score'] for item in result if item['category'] in target_categories)
        
        if (bonus_sum >= 63000):
            avg['BONUS'] += 1
            total += 35000
        
        s += total
        mn = min(total, mn)
        mx = max(total, mx)
        
    for key in avg:
        if (avg[key] >= 1000):
            avg[key] /= len(total_result)
    
    return avg, s / len(total_result), mx, mn

def get_all_match_data(datas):
    
    wincount = 0
    losecount = 0
    
    count = 1
    
    total_result = []
    all_my_bids = []      # 모든 게임의 내 배팅 금액
    all_opponent_bids = [] # 모든 게임의 상대방 배팅 금액
    
    for data in datas:
        game_data = load_game_data_from_file(data)

        match = re.search(rf'\[(FIRST|SECOND)\s+"{re.escape('Team 613')}"\]', game_data)
        team = match.group(1)
        
        game_result, my_bids, opponent_bids = parse_yacht_data(game_data, team)
        total_result.append(game_result)
        all_my_bids.extend(my_bids)
        all_opponent_bids.extend(opponent_bids)
        
        print('-----------------------------------------------------')
        
        print(f'{count}라운드 {wincount}승 {losecount}패 스테이지')
        match = re.search(r"SCOREFIRST (\d+)\nSCORESECOND (\d+)", game_data)
        if match:
            score_first = int(match.group(1))
            score_second = int(match.group(2))
            winner = "FIRST" if score_first > score_second else "SECOND"
            
            if winner == team:
                print('승리한 게임')
                wincount += 1

            else:
                print('패배한 게임')       
                losecount += 1 
        
        print()
        print_data(game_result)
        print()
        print_bid_analysis(my_bids, opponent_bids)
        print()
        
        count += 1
    
    avg, s, mx, mn = calculate_average(total_result)
    
    print('=====================================================')
    print(f'최종 전적 : {wincount}승 {losecount}패 (승률 {wincount / (wincount + losecount) * 100:.1f}%)')
    print()
    
    # 전체 배팅 평균 출력
    print('전체 배팅 분석:')
    if all_my_bids:
        my_total_avg = sum(all_my_bids) / len(all_my_bids)
        print(f"내 전체 배팅 평균: {my_total_avg:.1f} (총 {len(all_my_bids)}회)")
    
    if all_opponent_bids:
        opp_total_avg = sum(all_opponent_bids) / len(all_opponent_bids)
        print(f"상대 전체 배팅 평균: {opp_total_avg:.1f} (총 {len(all_opponent_bids)}회)")
    print()
    
    categorys = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'BONUS', 'CHOICE', 'FOUR_OF_A_KIND', 'FULL_HOUSE', 'SMALL_STRAIGHT', 'LARGE_STRAIGHT', 'YACHT']
    for category in categorys:
        print(f"{category} : {avg[category]}")
    
    print(f'평균 획득 점수 : {s:.0f}')
    print(f'최고 점수 : {mx}')
    print(f'최저 점수 : {mn}')

# 단일 게임 데이터 분석 함수 (예시 데이터용)
def analyze_single_game(game_data, team_name="Team 613"):
    """단일 게임 데이터를 분석"""
    # 팀이 FIRST인지 SECOND인지 확인
    match = re.search(rf'\[(FIRST|SECOND)\s+"{re.escape(team_name)}"\]', game_data)
    if not match:
        print(f"팀 '{team_name}'을 찾을 수 없습니다.")
        return
    
    my_team = match.group(1)
    opponent_team = "SECOND" if my_team == "FIRST" else "FIRST"
    
    # 상대팀 이름 찾기
    opponent_match = re.search(rf'\[{opponent_team}\s+"([^"]+)"\]', game_data)
    opponent_name = opponent_match.group(1) if opponent_match else "Unknown"
    
    print(f"내 팀: {team_name} ({my_team})")
    print(f"상대팀: {opponent_name} ({opponent_team})")
    print()
    
    game_result, my_bids, opponent_bids = parse_yacht_data(game_data, my_team)
    
    # 승부 결과
    match = re.search(r"SCOREFIRST (\d+)\nSCORESECOND (\d+)", game_data)
    if match:
        score_first = int(match.group(1))
        score_second = int(match.group(2))
        
        my_score = score_first if my_team == "FIRST" else score_second
        opp_score = score_second if my_team == "FIRST" else score_first
        
        result = "승리" if my_score > opp_score else "패배"
        print(f"게임 결과: {result} ({my_score} vs {opp_score})")
    print()
    
    # 점수 분석
    print("=== 점수 분석 ===")
    print_data(game_result)
    print()
    
    # 배팅 분석
    print("=== 배팅 분석 ===")
    print_bid_analysis(my_bids, opponent_bids)
