from dataclasses import dataclass
from typing import Dict, List, Callable, Optional

@dataclass
class Character:
    name: str
    affection: int = 0
    
@dataclass
class PlayerState:
    music_skill: int = 0
    # 其他玩家属性
    relationships: Dict[str, Character] = None
    
    def __post_init__(self):
        if self.relationships is None:
            self.relationships = {}

@dataclass
class Condition:
    type: str  # 'attribute', 'relationship', 'combination'
    operator: str  # '>', '<', '>=', '<=', '==', '!='
    value: int
    target: Optional[str] = None  # 用于relationship类型
    
    def evaluate(self, player_state: PlayerState) -> bool:
        actual_value = self._get_value(player_state)
        
        ops = {
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y,
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y,
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y
        }
        
        return ops[self.operator](actual_value, self.value)
    
    def _get_value(self, player_state: PlayerState) -> int:
        if self.type == 'attribute':
            return getattr(player_state, self.target)
        elif self.type == 'relationship':
            return player_state.relationships[self.target].affection
        raise ValueError(f"Unsupported condition type: {self.type}")

@dataclass
class ComplexCondition:
    conditions: List[Condition]
    operator: str = 'and'  # 'and' or 'or'
    
    def evaluate(self, player_state: PlayerState) -> bool:
        results = [cond.evaluate(player_state) for cond in self.conditions]
        if self.operator == 'and':
            return all(results)
        elif self.operator == 'or':
            return any(results)
        raise ValueError(f"Unsupported operator: {self.operator}")

@dataclass
class Choice:
    text: str
    next_scene: str
    conditions: Optional[ComplexCondition] = None
    effects: Optional[Dict[str, int]] = None

class Scene:
    def __init__(self, scene_id: str, content: str, choices: List[Choice]):
        self.scene_id = scene_id
        self.content = content
        self.choices = choices
        
    def is_choice_available(self, choice: Choice, player: PlayerState) -> bool:
        if not choice.conditions:
            return True
            
        for attr, required_value in choice.conditions.items():
            if attr.startswith('affection_'):
                char_name = attr.replace('affection_', '')
                if player.relationships[char_name].affection < required_value:
                    return False
            elif attr == 'music_skill' and player.music_skill < required_value:
                return False
        return True

class StoryEngine:
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.player = PlayerState()
        self.current_scene: Optional[Scene] = None
        
    def add_scene(self, scene: Scene):
        self.scenes[scene.scene_id] = scene
        
    def start_game(self, first_scene_id: str):
        self.current_scene = self.scenes[first_scene_id]
        
    def make_choice(self, choice_index: int) -> str:
        choice = self.current_scene.choices[choice_index]
        
        # 应用选择的效果
        if choice.effects:
            for attr, value in choice.effects.items():
                if attr.startswith('affection_'):
                    char_name = attr.replace('affection_', '')
                    self.player.relationships[char_name].affection += value
                elif attr == 'music_skill':
                    self.player.music_skill += value
                    
        # 转到下一个场景
        self.current_scene = self.scenes[choice.next_scene]
        return self.current_scene.content 