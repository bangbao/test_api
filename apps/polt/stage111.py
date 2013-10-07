# coding: utf-8
from instantft.battle.polt import Polt
opening = Polt() #开始的对话
opening.set_mapinfo(11, 5) #先设置地图大小
a1=opening.add_agent(10046,7,2) #添加人 淘气巨魔1
a2=opening.add_agent(10046,6,3) #添加人 淘气巨魔2
a3=opening.add_agent(10046,8,3) #添加人 淘气巨魔3
d1=opening.add_agent(50016,7,3) #添加人  闪电魔球
d2=opening.add_agent(221,1,3) #添加人（hero id,x,y）   法师杀手

opening.set_atk_group(a1,a2,a3) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_left(a1,a3)  #设置朝向 上边和右边的巨魔向左
opening.face_to_right(a2,d1,d2) #朝向,魔球和左边的巨魔向右。如果转向在后面的new_frame里新设

opening.move(a1,[(1,3),(3,3)],2)
opening.dialog(a2, "饿…冷…老大他自己跑路了！") 
opening.idle(a3)
opening.idle(d1)
opening.new_frame()

opening.idle(a1)
opening.idle(a2)
opening.dialog(a3, "别怕！俺偷了这个，来生个火……")
opening.idle(d1)
opening.new_frame()

opening.dialog(d2,"莫非是宝物？")
d3= opening.birth_agent(10022,12,1) #添加人（hero id,x,y）   狗娃
d4= opening.birth_agent(10022,12,5) #添加人（hero id,x,y）   狗娃
opening.set_def_group(d3,d4) #把哪些人分为一组  a 攻击组 d防守组
opening.face_to_left(d3,d4) #朝向,魔球和左边的巨魔向右。如果转向在后面的new_frame里新设
opening.face_to_right(a1,a2,a3)  #设置朝向所有巨魔向左
opening.dialog(a1, "什么人？")
opening.dialog(a2, "！")
opening.dialog(a3, "！")
opening.idle(d1)
opening.new_frame()

opening.dialog(d3,"这儿有肉味！")
opening.dialog(d4,"弟兄们上！")
opening.idle(d1)
opening.idle(d2)
opening.idle(a1)
opening.idle(a2)
opening.idle(a3) 

takeabow=Polt()
takeabow.set_mapinfo(11, 5) #先设置地图大小
a1=takeabow.add_agent(10046,7,2) #添加人 淘气巨魔1 活着
a2=takeabow.add_agent(10046,6,3) #添加人 淘气巨魔2 死的
a3=takeabow.add_agent(211,3,3)   #添加人 法师杀手 活的
d1=takeabow.add_agent(10022,8,4) #添加人  狗头1 死的
d2=takeabow.add_agent(10022,9,5) #添加人  狗头2 死的

takeabow.set_atk_group(a1,a2,a3) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_left(a1,d1,d2)  #设置朝向 狗头向左，活巨魔向左
takeabow.face_to_right(a2,a3) #朝向,死巨魔向右。如果转向在后面的new_frame里新设

takeabow.dead(a2,d1,d2)
takeabow.dialog(a1, "客官不可以!","我上有老下有小……会生火会烧肉会洗衣会暖床，英雄饶命啊！")
takeabow.dialog(a3,"矮油…我这个人心最软了，先跟我混吧")
