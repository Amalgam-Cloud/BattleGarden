import re
from main import *
from f_u_c_k_base import *
#Ingrid
class Blanked_Spray(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= -1, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.targets = None
    def insert(self,battle_chain, chain= "", targets= None,receivers=None):
        self.counter += 1
        if (self.counter <= 1):
            self.targets = targets
            #print(chain, self.say_hi())
            battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, "-> (Blanked Spray)")
        print("Enemy Team: ")
        for target in Action.choose_all_enemy_targets(self, targets=self.targets):
            Token.increase(owner= target, token= Fulfillment_Token, n= 2, sender= self.sender)
        print()
class Water_Blast(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= 0, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.reciever = None
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        self.counter += 1
        if (self.counter <= 3):
            #print(chain, self.say_hi())
            self.receiver = receiver if receiver != None else self.choose_random_enemy_target(targets= targets)
            battle_chain.append(self)
            return re.sub(self.mask,'@',chain,1)
        return chain
    def on(self):
        print(self.sender.name, "-> (Water Blast) ->",self.receiver.name)
        print(self.receiver.name,"-> + 1",self.lang['d_d'])
        self.receiver.distant_damage += 1
        Token.increase(owner= self.receiver, token= Fulfillment_Token, n=1, sender= self.sender)
class Froze_Up(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= 1, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.targets = None
    def insert(self,battle_chain, chain= "", targets= None,receivers=None):
        self.counter += 1
        if (self.counter <= 1):
            self.targets = targets
            #print(chain, self.say_hi())
            battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, "-> (Froze Up)")
        print("Enemy Team: ")
        for target in Action.choose_all_enemy_targets(self, targets=self.targets):
            if(target.find_token(Fulfillment_Token) != None):
                val = target.find_token(Fulfillment_Token).value
                if(val >= 4):
                    if(target.actions != []):
                        print(target.name, ":", str(type(random.choice(target.actions))))
                        act = random.choice(target.actions)
                        target.actions.remove(act)
                        target.find_token(Fulfillment_Token).release_all()
                    elif(val >= 2):
                        print(target.name,self.lang['cond_s'])
                        target.tokens.append(Stun_Token(value=1,owner=target))
                        target.find_token(Fulfillment_Token).release_all()
                elif(val >= 2):
                    print(target.name,self.lang['cond_s'])
                    Token.increase(owner=target,token=Stun_Token,n= 1,sender= self.sender)
                    target.find_token(Fulfillment_Token).release_all()
        print()
#Lary
class Legioner_Judge(Action):
    def __init__(self,sender,mask, mask_size, lang, reciever= None,action_class= -1, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.targets = None
    def insert(self,battle_chain, chain= "", targets= None,receivers=None):
        if(self.sender.find_token(Arrow_Token) != None and self.sender.find_token(Arrow_Token).value > 0):
            self.counter += 1
            if (self.counter <= 1):
                self.targets = targets
                #print(chain, self.say_hi())
                battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, "-> (Legioner Judge)")
        print(self.sender.name, "-> -1",self.lang['a'])
        self.sender.find_token(Arrow_Token).release()
        print("Enemy Team: ")
        for target in Action.choose_all_enemy_targets(self, targets=self.targets):
            print(target.name,":",target.distant_damage,"->", target.distant_damage + self.sender.distant_power,self.lang['d_d'])
            target.distant_damage += self.sender.distant_power
        print()
class Blinking_Daggers(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= -1, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.sender = sender
    def insert(self,battle_chain, chain= "", targets= None,receivers=None):
        self.counter += 1
        if (self.counter <= 1):
            #print(chain, self.say_hi())
            battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, "-> (Blinking Daggers)")
        print(self.sender.name, ":", self.lang['blink_dagger_1'],"\n")
        self.sender.find_action(Stab).counter = -999
class Power_Shoot(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= 0, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.reciever = None
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        if (self.sender.find_token(Arrow_Token) != None and self.sender.find_token(Arrow_Token).value > 0):
            self.counter += 1
            if (self.counter <= 3):
                #print(chain, self.say_hi())
                self.receiver = receiver if receiver != None else self.choose_random_enemy_target(targets= targets)
                battle_chain.append(self)
                return re.sub(self.mask,'@@',chain,1)
        return chain
    def on(self):
        print(self.sender.name, "-> (Power Shoot) ->",self.receiver.name)
        print(self.sender.name, "-> -1",lang['a'])
        self.sender.find_token(Arrow_Token).release()
        print(self.receiver.name,"-> +",self.sender.distant_power,lang['d_d'],"\n")
        self.receiver.distant_damage += self.sender.distant_power
        #Add revenge counter on enemy
        #for counter in receiver.counters:
            #if(type(counter) == Revenge_Counter and counter.owner == self.sender):
                #counter.increase()
                #break
class Stab(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= 0, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.reciever = None
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        self.counter += 1
        if (self.counter <= 3):
            #print(chain, self.say_hi())
            self.receiver = receiver if receiver != None else self.choose_random_enemy_target(targets= targets)
            battle_chain.append(self)
            return re.sub(self.mask,'@@',chain,1)
        return chain
    def on(self):
        print(self.sender.name, "-> (Stab) -> ",self.receiver.name)
        print(self.receiver.name,"-> +",self.sender.attack_power,self.lang['p_d'],"\n")
        self.receiver.pure_damage += self.sender.attack_power
        #Add revenge counter on enemy
        #for counter in receiver.counters:
            #if(type(counter) == Revenge_Counter and counter.owner == self.sender):
                #counter.increase()
                #break
#Fafnir
class Group_Up(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= -1, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.targets = []
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        self.targets = targets
        self.counter += 1
        if (self.counter <= 1):
            #print(chain, self.say_hi())
            battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, "-> (Group Up!)")
        print("Team:")
        for target in Action.choose_all_fellow_targets(self,owner= self.sender, targets= self.targets):
            print(target.name,":",target.cur_shield,"->",target.cur_shield + 2,self.lang['p_s'],"\n")
            target.cur_shield += 2
class Swing_Slash(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= 0, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.targets = None
    def insert(self,battle_chain, chain= "", targets= None,receivers=None):
        self.counter += 1
        if (self.counter <= 1):
            self.targets = targets
            #print(chain, self.say_hi())
            battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, "-> (Swing Slash)")
        print("Enemy Team: ")
        for target in Action.choose_all_enemy_targets(self, targets=self.targets):
            print(target.name,":",target.physic_damage,"->", target.physic_damage + self.sender.attack_power,self.lang['p_d'])
            target.physic_damage += target.attack_power
        print()
class Force_Attack(Action):
    def __int__(self, sender, mask, mask_sized,lang, action_class=0, counter= 0):
        Action.__int__(self,sender= sender,mask= mask, mask_sized= mask_sized, action_class= action_class, counter= counter, lang= lang)
    def insert(self,battle_chain, chain= "", targets= None, receiver= None):
        self.counter += 1
        if(self.counter <= 3):
            #print(chain, self.say_hi())
            self.receiver = receiver if receiver != None else self.choose_random_enemy_target(targets= targets)
            battle_chain.append(self)
            return re.sub(self.mask,'@@',chain,1)
        return chain
    def on(self):
        print(self.sender.name, "-> (Force Attack) ->",self.receiver.name)
        print(self.receiver.name,"-> +",self.sender.attack_power,self.lang['p_d'])
        self.receiver.physic_damage += self.sender.attack_power
        if(round(self.sender.protect_power/2) > 0):
            print(self.sender.name, "-> +", round(self.sender.protect_power/2),self.lang['p_s'] ,"\n")
            self.sender.cur_shield += round(self.sender.protect_power/2)
        else:
            print(self.sender.name, "-> +1",self.lang['p_s'],"\n")
            self.sender.cur_shield += 1
#Wolf
class Bite(Action):
    def __init__(self,sender,mask, mask_size,lang,reciever= None,action_class= 0, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.reciever = None
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        self.counter += 1
        if (self.counter <= 2):
            #print(chain, self.say_hi())
            self.receiver = receiver if receiver != None else self.choose_weakest_enemy_tagret(targets= targets)
            battle_chain.append(self)
            return re.sub(self.mask,'@@',chain,1)
        return chain
    def on(self):
        print(self.sender.name, "-> (Bite) -> ",self.receiver.name)
        print(self.receiver.name,"-> +",self.sender.attack_power,self.lang['p_d'],"\n")
        Token.increase(owner= self.receiver,token= Bleedness_Token,n=1, sender= self.receiver)
        self.receiver.physic_damage += self.sender.attack_power
        #Add revenge counter on enemy
        #for counter in receiver.counters:
            #if(type(counter) == Revenge_Counter and counter.owner == self.sender):
                #counter.increase()
                #break
