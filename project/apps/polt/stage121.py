# coding: utf-8
from instantft.battle.polt import Polt
opening = Polt() #开始的对话
opening.set_mapinfo(11, 5) #先设置地图大小

a1=opening.add_agent(221,3,3) #添加人  法师杀手
d1=opening.add_agent(10013,10,2) #添加   人马娃娃 活的
d2=opening.add_agent(10016,10,5) #添加    人马他妈 活的

opening.set_atk_group(a1) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_right(a1)  #朝向。巨魔都向右。
opening.face_to_left(d1,d2)  #朝向。人马都向左。

opening.dialog(d1, "嚯！")
opening.dialog(a1, "哈？")
opening.idle(d2)
opening.new_frame()

opening.dialog(d1, "路边的野花你不要采！")
opening.dialog(d2, "要想从此过，留下买路财！")
opening.dialog(a1,"不就打个劫…有必要这么多花样吗！")

takeabow =Polt() #结束的对话
takeabow.set_mapinfo(11, 5) #先设置地图大小
a1=takeabow.add_agent(221,6,3) #添加人  法师杀手
d1=takeabow.add_agent(10013,7,3) #添加英雄 人马娃娃
d2=takeabow.add_agent(10016,9,5) #添加英雄 人马他妈

takeabow.set_atk_group(a1) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_left(a1)  #法师杀手向左
takeabow.face_to_right(d1,d2) #剑王、法师杀手向右。

takeabow.attack2(a1,d1,"melee_effect_01")   #法师杀手第2种普通攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
takeabow.hurt(d1,"melee_effect_01",1200)  #受击 （self, hero代号, 填skill_data里的effect_lua ,掉的血量）
takeabow.dialog(d2,"！")
takeabow.new_frame()

takeabow.dead(d1)
takeabow.dialog(d2,"我错了！有眼不识大神，这件装备请大神笑纳!")
takeabow.dialog(a1,"哦─.─||  那我问你，人马不是住在内陆的马利戈壁上吗。怎么会跑到雪域来？ ")
takeabow.new_frame()

takeabow.dialog(d2,"呜呜…一群黑皮巨魔跑来凶巴巴赶我们走咯，不然也不会跑到这鸟不拉屎的鬼地方来T T")
takeabow.dialog(a1,"什么？莫非雪域要塞已经被攻破啦?必须回去!")
