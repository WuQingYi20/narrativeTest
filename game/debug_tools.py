from typing import List, Dict, Set
from copy import deepcopy
from story_engine import StoryEngine, PlayerState, Scene
import json

class DebugTools:
    def __init__(self, engine: StoryEngine):
        self.engine = engine
        
    def analyze_story_branches(self) -> Dict:
        """分析所有可能的剧情分支路径"""
        visited_scenes = set()
        paths = []
        
        def dfs(scene_id: str, current_path: List, player_state: PlayerState):
            if scene_id in visited_scenes:
                return
                
            visited_scenes.add(scene_id)
            current_scene = self.engine.scenes[scene_id]
            current_path.append(scene_id)
            
            for choice in current_scene.choices:
                if current_scene.is_choice_available(choice, player_state):
                    # 创建新的玩家状态来模拟这个选择
                    new_state = deepcopy(player_state)
                    self._apply_effects(choice.effects, new_state)
                    dfs(choice.next_scene, current_path.copy(), new_state)
            
            paths.append({
                'path': current_path,
                'player_state': self._serialize_state(player_state)
            })
        
        dfs('start', [], deepcopy(self.engine.player))
        return {
            'total_paths': len(paths),
            'paths': paths
        }
    
    def simulate_playthrough(self, choices: List[int]) -> Dict:
        """模拟特定选择序列的游戏流程"""
        engine_copy = deepcopy(self.engine)
        engine_copy.start_game('start')
        
        history = []
        
        try:
            for choice_index in choices:
                current_state = {
                    'scene_id': engine_copy.current_scene.scene_id,
                    'content': engine_copy.current_scene.content,
                    'player_state': self._serialize_state(engine_copy.player)
                }
                history.append(current_state)
                
                engine_copy.make_choice(choice_index)
                
            return {
                'success': True,
                'history': history,
                'final_state': self._serialize_state(engine_copy.player)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'history': history
            }
    
    def check_unreachable_scenes(self) -> Set[str]:
        """检查无法到达的场景"""
        reachable_scenes = set()
        
        def traverse(scene_id: str, player_state: PlayerState):
            if scene_id in reachable_scenes:
                return
                
            reachable_scenes.add(scene_id)
            current_scene = self.engine.scenes[scene_id]
            
            for choice in current_scene.choices:
                if current_scene.is_choice_available(choice, player_state):
                    new_state = deepcopy(player_state)
                    self._apply_effects(choice.effects, new_state)
                    traverse(choice.next_scene, new_state)
        
        traverse('start', deepcopy(self.engine.player))
        return set(self.engine.scenes.keys()) - reachable_scenes
    
    def validate_story_consistency(self) -> Dict:
        """验证剧情的一致性"""
        issues = []
        
        # 检查场景引用
        for scene_id, scene in self.engine.scenes.items():
            for choice in scene.choices:
                if choice.next_scene not in self.engine.scenes:
                    issues.append(f"场景 '{scene_id}' 中的选项引用了不存在的场景 '{choice.next_scene}'")
        
        # 检查角色引用
        all_characters = set(self.engine.player.relationships.keys())
        for scene in self.engine.scenes.values():
            for choice in scene.choices:
                if choice.effects:
                    for effect in choice.effects:
                        if effect.startswith('affection_'):
                            char_name = effect.replace('affection_', '')
                            if char_name not in all_characters:
                                issues.append(f"选项效果引用了未定义的角色 '{char_name}'")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    @staticmethod
    def _serialize_state(player_state: PlayerState) -> Dict:
        """序列化玩家状态为可读格式"""
        return {
            'music_skill': player_state.music_skill,
            'relationships': {
                name: {'name': char.name, 'affection': char.affection}
                for name, char in player_state.relationships.items()
            }
        }
    
    @staticmethod
    def _apply_effects(effects: Dict[str, int], player_state: PlayerState):
        """应用效果到玩家状态"""
        if not effects:
            return
            
        for attr, value in effects.items():
            if attr.startswith('affection_'):
                char_name = attr.replace('affection_', '')
                player_state.relationships[char_name].affection += value
            elif attr == 'music_skill':
                player_state.music_skill += value 
    
    def analyze_game_balance(self) -> Dict:
        """分析游戏数值平衡性"""
        stats = {
            'attribute_ranges': {
                'music_skill': {'min': float('inf'), 'max': float('-inf')},
            },
            'relationship_ranges': {},
            'choice_availability': {},
            'path_analysis': [],
            'bottlenecks': []
        }
        
        # 初始化关系数值范围
        for char in self.engine.player.relationships:
            stats['relationship_ranges'][char] = {
                'min': float('inf'),
                'max': float('-inf')
            }
        
        def analyze_path(scene_id: str, path: List, player_state: PlayerState, depth: int = 0):
            if depth > 20:  # 防止无限循环
                return
                
            current_scene = self.engine.scenes[scene_id]
            
            # 更新属性范围
            stats['attribute_ranges']['music_skill']['min'] = min(
                stats['attribute_ranges']['music_skill']['min'],
                player_state.music_skill
            )
            stats['attribute_ranges']['music_skill']['max'] = max(
                stats['attribute_ranges']['music_skill']['max'],
                player_state.music_skill
            )
            
            # 更新关系范围
            for char, relationship in player_state.relationships.items():
                stats['relationship_ranges'][char]['min'] = min(
                    stats['relationship_ranges'][char]['min'],
                    relationship.affection
                )
                stats['relationship_ranges'][char]['max'] = max(
                    stats['relationship_ranges'][char]['max'],
                    relationship.affection
                )
            
            # 分析选项可用性
            available_choices = []
            for choice in current_scene.choices:
                if current_scene.is_choice_available(choice, player_state):
                    available_choices.append(choice)
            
            # 记录选项可用性
            choice_key = f"{scene_id}"
            if choice_key not in stats['choice_availability']:
                stats['choice_availability'][choice_key] = {
                    'total_choices': len(current_scene.choices),
                    'available_count': len(available_choices),
                    'player_state': self._serialize_state(player_state)
                }
            
            # 检测瓶颈（所有选项都不可用的情况）
            if len(available_choices) == 0 and len(current_scene.choices) > 0:
                stats['bottlenecks'].append({
                    'scene_id': scene_id,
                    'player_state': self._serialize_state(player_state)
                })
            
            # 记录路径分析
            path_stats = {
                'path': path + [scene_id],
                'final_state': self._serialize_state(player_state),
                'choices_available': len(available_choices),
                'depth': depth
            }
            stats['path_analysis'].append(path_stats)
            
            # 继续遍历可用选项
            for choice in available_choices:
                new_state = deepcopy(player_state)
                self._apply_effects(choice.effects, new_state)
                analyze_path(choice.next_scene, path + [scene_id], new_state, depth + 1)
        
        # 开始分析
        analyze_path('start', [], deepcopy(self.engine.player))
        
        # 计算一些统计信息
        stats['summary'] = {
            'total_scenes': len(self.engine.scenes),
            'total_paths_analyzed': len(stats['path_analysis']),
            'bottleneck_count': len(stats['bottlenecks']),
            'average_choices_per_scene': sum(
                s['available_count'] for s in stats['choice_availability'].values()
            ) / len(stats['choice_availability'])
        }
        
        return stats
    
    def suggest_balance_improvements(self) -> List[str]:
        """基于数值分析提供平衡性改进建议"""
        analysis = self.analyze_game_balance()
        suggestions = []
        
        # 检查属性范围
        music_skill_range = analysis['attribute_ranges']['music_skill']
        if music_skill_range['max'] - music_skill_range['min'] > 10:
            suggestions.append(
                f"音乐技能范围可能过大 ({music_skill_range['min']} - {music_skill_range['max']})，"
                "建议缩小差距以保持平衡"
            )
        
        # 检查关系值范围
        for char, ranges in analysis['relationship_ranges'].items():
            if ranges['max'] - ranges['min'] > 15:
                suggestions.append(
                    f"角色 {char} 的好感度范围过大 ({ranges['min']} - {ranges['max']})，"
                    "可能导致剧情体验不稳定"
                )
        
        # 检查选项可用性
        for scene_id, availability in analysis['choice_availability'].items():
            if availability['available_count'] < availability['total_choices'] * 0.5:
                suggestions.append(
                    f"场景 {scene_id} 的可用选项比例过低 "
                    f"({availability['available_count']}/{availability['total_choices']})，"
                    "建议调整选项条件或增加替代选项"
                )
        
        # 检查瓶颈
        if analysis['bottlenecks']:
            suggestions.append(
                f"发现 {len(analysis['bottlenecks'])} 个剧情瓶颈，"
                "这些场景在某些状态下没有可用选项"
            )
        
        return suggestions

    def test_specific_scenario(self, initial_state: Dict[str, int], choices: List[int]) -> Dict:
        """测试特定场景下的游戏体验"""
        # 创建一个具有指定初始状态的引擎副本
        test_engine = deepcopy(self.engine)
        
        # 设置初始状态
        for attr, value in initial_state.items():
            if attr.startswith('affection_'):
                char_name = attr.replace('affection_', '')
                test_engine.player.relationships[char_name].affection = value
            else:
                setattr(test_engine.player, attr, value)
        
        # 运行模拟
        return self.simulate_playthrough(choices)