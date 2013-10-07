# coding: utf-8

class BaseAgent(object):
    """ 基础战斗单位对象

      每套环境都需要实现一个BaseAgent的子类，来控制所有战斗单位的
    动作.
    """

    def attack(self, *targets):
        """ 统一的攻击接口
        """

        raise NotImplementedError

    def skill(self):
        """ 统一的技能接口
        """

        raise NotImplementedError

    def under_attack(self, atk_type, atk_value):
        """ 受到某种类型的攻击

        Args:
            atk_type: 攻击类型，普通攻击或魔法攻击
            atk_value: 受到攻击的数值
        """

        raise NotImplementedError
