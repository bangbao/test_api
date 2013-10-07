# coding: utf-8
from instantft.battle.polt import Polt
opening =Polt()  #开始的对话

opening.set_mapinfo(11, 5) #先设置地图大小
a1=opening.add_agent(137,3,3) #添加人  剑王
a2=opening.add_agent(10046,4,4) #添加人  淘气巨魔
d1=opening.add_agent(10052,7,3) #添加   下流巨魔 活的
d2=opening.add_agent(10016,9,4) #添加    食尸鬼 活的

opening.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_right(a1,a2)  #朝向。都向右。
opening.face_to_left(d1,d2)  #朝向。巨魔都向左。

opening.dialog(d1, "鲜肉！")
opening.dialog(d2, "呜嗷嗷！！ 嗷 嗷嗷嗷！！！！")
opening.new_frame()

opening.dialog(a1, "小子注意！不要被咬了！")
opening.dialog(a2, "这什么东西！？")

takeabow =Polt()   #结束的对话

takeabow.set_mapinfo(11, 5) #先设置地图大小
a1=takeabow.add_agent(137,5,3) #添加人  剑王
a2=takeabow.add_agent(10046,4,5) #添加人  淘气巨魔
d1=takeabow.add_agent(10052,4,2) #添加   下流巨魔 活的
d2=takeabow.add_agent(10016,6,3) #添加    食尸鬼 活的

takeabow.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_right(a1,a2)  #朝向。都向右。
takeabow.face_to_left(d1,d2)  #朝向。巨魔都向左。

takeabow.dead(d1,d2)
takeabow.dialog(a1, "如此渣的食尸鬼，御主的实力也是一般！")
takeabow.dialog(a2, "鱼煮是啥，可以吃吗？")
takeabow.new_frame()

takeabow.dialog(a1, "哈，两个天谴宝宝，可以炼制更强的死灵生物！")
takeabow.idle(a2)