from story_engine import ComplexCondition, Condition, Scene, Choice, StoryEngine, Character

def init_story() -> StoryEngine:
    engine = StoryEngine()
    
    # 初始化角色
    engine.player.relationships['yuki'] = Character('Yuki')
    engine.player.relationships['mei'] = Character('Mei')
    
    # 示例场景
    scene1 = Scene(
        'start',
        '你站在音乐教室门口，犹豫要不要进去...',
        [
            Choice(
                '鼓起勇气走进去',
                'music_room_enter',
                effects={'music_skill': 1}
            ),
            Choice(
                '在门外偷听一会',
                'eavesdrop',
                effects={'affection_yuki': -1}
            )
        ]
    )
    
    scene2 = Scene(
        'music_room_enter',
        '优木同学正在练习钢琴...',
        [
            Choice(
                '赞美她的演奏',
                'praise_playing',
                conditions={'music_skill': 2},
                effects={'affection_yuki': 2}
            ),
            Choice(
                '默默坐在一旁听她弹琴',
                'quiet_listening',
                effects={'music_skill': 1, 'affection_yuki': 1}
            )
        ]
    )
    
    complex_scene = Scene(
        'complex_choice',
        '你遇到了一个重要的决定...',
        [
            Choice(
                '选择A',
                'scene_a',
                conditions=ComplexCondition([
                    Condition('relationship', '>=', 5, 'yuki'),
                    Condition('attribute', '>=', 3, 'music_skill')
                ], 'and')
            ),
            Choice(
                '选择B',
                'scene_b',
                conditions=ComplexCondition([
                    Condition('relationship', '>=', 3, 'mei'),
                    Condition('relationship', '<', 0, 'yuki')
                ], 'or')
            )
        ]
    )
    
    engine.add_scene(scene1)
    engine.add_scene(scene2)
    engine.add_scene(complex_scene)
    # 添加更多场景...
    
    return engine 