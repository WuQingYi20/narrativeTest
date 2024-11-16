from story_data import init_story

def main():
    engine = init_story()
    engine.start_game('start')
    
    while True:
        print("\n" + engine.current_scene.content)
        
        # 显示可用选项
        available_choices = [
            (i, choice) for i, choice in enumerate(engine.current_scene.choices)
            if engine.current_scene.is_choice_available(choice, engine.player)
        ]
        
        for i, choice in available_choices:
            print(f"{i + 1}. {choice.text}")
            
        # 获取玩家输入
        choice = int(input("请选择 (输入数字): ")) - 1
        engine.make_choice(choice)

if __name__ == "__main__":
    main() 