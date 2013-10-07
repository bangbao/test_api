# coding: utf-8
from instantft.battle.polt import Polt
opening = None #开始的对话

takeabow =Polt() #结束的对话
takeabow.set_mapinfo(11, 5) #先设置地图大小

a1=takeabow.add_agent(137,3,3) #添加人  剑王
a2=takeabow.add_agent(10046,4,4) #添加人  淘气巨魔
d1=takeabow.add_agent(10052,7,3) #添加   下流巨魔 活的
d2=takeabow.add_agent(10016,9,4) #添加    人马他妈 活的

takeabow.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_right(d1,a1,a2)  #朝向。都向右。
takeabow.face_to_left(d2)  #朝向。人马都向左。

takeabow.attack2(d1,d2,"range_xialiu")   #法师杀手第2种普通攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
takeabow.hurt(d2,"range_xialiu",600)  #受击 （self, hero代号, 填skill_data里的effect_lua ,掉的血量）
takeabow.dialog(a2, "又黑我大巨魔！…额…怎么又是黑巨魔！")
takeabow.dialog(a1,"NND……（天灾军团里什么时候混进去这种烂货……）")
takeabow.new_frame()

takeabow.dead(d2)
takeabow.face_to_left(d1)  #朝向。下流巨魔向左。
takeabow.dialog(d1, "鲜肉！咬咬咬！")
takeabow.dialog(a2, "从没见过这种妖术！到底发生了什么…")
takeabow.dialog(a1, "走吧小家伙，只要追上他们！到时候就知道了！")