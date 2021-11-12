import random

from functools import cmp_to_key
from random import randint
from Heroes import *
from f_u_c_k_base import *



#Debutes
class Raise_Up(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= -1, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.reciever = None
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        self.counter += 1
        if (self.counter <= 3):
            #print(chain, self.say_hi())
            self.receiver = receiver if receiver != None else self.choose_random_fellow_target(owner= self.sender,targets= targets)
            battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, " -> (Raise Up) -> ",self.receiver.name)
        print(self.sender.name,":",self.sender.attack_power,"->",self.sender.attack_power * 2,self.lang['power'])
        self.receiver.attack_power *= 2
class Heavens_Mercy(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= -1, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang= lang)
        self.targets = []
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        self.targets = targets
        self.counter += 1
        if (self.counter <= 3):
            #print(chain, self.say_hi())
            battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, "-> (Heavens Mercy)")
        print("Team:")
        for target in Action.choose_all_fellow_targets(self,owner= self.sender, targets= self.targets):
            if(target.cur_HP < target.HP):
                print(target.name,":",target.cur_HP,"->",target.cur_HP + 1,"HP")
                target.cur_HP += 1
class Holy_Shield(Action):
    def __init__(self,sender,mask, mask_size, lang, reciever= None,action_class= -1, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang=lang)
        self.targets = []
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        self.targets = targets
        self.counter += 1
        if (self.counter <= 3):
            #print(chain, self.say_hi())
            battle_chain.append(self)
        return chain
    def on(self):
        print(self.sender.name, "-> (Holy Shield)")
        print("Team:")
        for target in Action.choose_all_fellow_targets(self,owner= self.sender, targets= self.targets):
            print(target.name,":",target.cur_shield,"->",target.cur_shield + 1,self.lang['shields'])
            target.cur_shield += 1

#Bravades
class Attack(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= 0, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang=lang)
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
        print(self.sender.name, "-> (Attack) ->",self.receiver.name)
        print(self.receiver.name,"-> +",self.sender.attack_power,self.lang['p_d'],"\n")
        self.receiver.physic_damage += self.sender.attack_power
        #Add revenge counter on enemy
        #for counter in receiver.counters:
            #if(type(counter) == Revenge_Counter and counter.owner == self.sender):
                #counter.increase()
                #break
class Protect(Action):
    def __init__(self, sender, mask,mask_size,lang, action_class= 0, counter= 0):
        Action.__init__(self,sender=sender, mask=mask, mask_size= mask_size, action_class= action_class, counter= counter,lang=lang)
    def insert(self,battle_chain, chain= "", targets= None):
        self.counter += 1
        if (self.counter <= 2):
            #print(chain, self.say_hi())
            battle_chain.append(self)
            return re.sub(self.mask,'@',chain,1)
        return chain
    def on(self):
        print(self.sender.name,"-> (Protect)")
        print(self.sender.name,"-> +",self.sender.protect_power,self.lang['shields'])
        self.sender.cur_shield += self.sender.protect_power
        print()
class Pierce(Action):
    def __init__(self,sender,mask, mask_size,lang, reciever= None,action_class= 0, counter= 0):
        Action.__init__(self,sender=sender,mask= mask, mask_size= mask_size, action_class= action_class, counter= counter, lang=lang)
        self.reciever = None
    def insert(self,battle_chain, chain= "", targets= None,receiver=None):
        self.counter += 1
        if (self.counter <= 3):
            #print(re.sub(self.mask,'@',chain,1), self.say_hi())
            self.receiver = receiver if receiver != None else self.choose_random_enemy_target(targets= targets)
            battle_chain.append(self)
            return re.sub(self.mask,'@',chain,1)
        return chain
    def on(self):
        print(self.sender.name, "-> (Pierce) ->",self.receiver.name)
        print(self.receiver.name,"-> +",self.sender.attack_power,self.lang['p_d'],"\n")
        self.receiver.pure_damage += round(self.sender.attack_power) if round(self.sender.attack_power)>0 else 1
        #Add revenge counter on enemy
        #for counter in receiver.counters:
            #if(type(counter) == Revenge_Counter and counter.owner == self.sender):
                #counter.increase()
                #break

class BattleField:
    def __init__(self,characters,lang):
        self.lang = lang
        self.characters = characters
        self.battle_chain = []
        self.teams = []
        self.sum_potential = 0
        for char in self.characters:
            self.sum_potential += char.potential
            if(not(char.team_id in self.teams)):
                self.teams.append(char.team_id)
        Revenge_Token.create_revenge_field(characters= characters, lang=lang)
    def turn_round(self, insert_chain, mode):
        #Initialize
        for char in self.characters:
            if(mode == 0):
                char.cur_initiative = randint(1,20)
            else:
                print(char.name,self.lang['init'])
                char.cur_initiative = int(input())
        self.characters = sorted(self.characters, key=cmp_to_key(lambda char1, char2: char2.cur_initiative - char1.cur_initiative))
        #Release debute counters
        for char in self.characters:
            char.activate_counters(-1)
        #Fullfill debute,bravada and requiem
        debute_queue = []
        bravada_queue = []
        requiem_queue = []
        for i in range(len(self.characters)):
            if(self.characters[i].find_token(Stun_Token).value == 0):
                for j in range(len(self.characters[i].actions)):
                    if(self.characters[i].actions[j].action_class == -1):
                        debute_queue.append(self.characters[i].actions[j])
                    elif(self.characters[i].actions[j].action_class == 0):
                        bravada_queue.append(self.characters[i].actions[j])
                    elif(self.characters[i].actions[j].action_class == 1):
                        requiem_queue.append(self.characters[i].actions[j])
                    else:
                        raise ValueError("Action doesn't has purpose",self.characters[i].actions[j].say_hi())
        debute_queue.reverse()
        bravada_queue.reverse()
        requiem_queue.reverse()
        #Start debute
        #print("Prepare debute phase: \n")
        current_chain = insert_chain
        self.battle_chain = []
        for i in range(len(debute_queue)):
            act = debute_queue.pop()
            current_chain = Creature.try_act(act=act, cur_chain=current_chain,
                                             cur_party=self.characters,
                                             battle_chain=self.battle_chain)
        print("--------------------------------------------------------------------------------------------------")
        print(self.lang['deb_phase'],"\n")
        for i in range(len(self.battle_chain)):
            self.battle_chain.pop().on()
        #Prepare bravada
        #print("Prepare bravada phase: \n")
        for i in range(len(bravada_queue) - 1).__reversed__():
            for j in range(i, len(bravada_queue) - 1):
                if (bravada_queue[j].mask_size > bravada_queue[j + 1].mask_size):
                    temp = bravada_queue[j]
                    bravada_queue[j] = bravada_queue[j + 1]
                    bravada_queue[j + 1] = temp
                else:
                    break
        self.battle_chain = []
        for i in range(len(bravada_queue)):
            act = bravada_queue.pop()
            current_chain = Creature.try_act(act= act, cur_chain=current_chain, cur_party=self.characters,
                                            battle_chain=self.battle_chain)
        #Prepare chain by order
        for i in range(len(self.battle_chain)-1).__reversed__():
            for j in range(i,len(self.battle_chain)-1):
                if (self.battle_chain[j].sender.cur_initiative > self.battle_chain[j+1].sender.cur_initiative):
                    temp = self.battle_chain[j]
                    self.battle_chain[j] = self.battle_chain[j + 1]
                    self.battle_chain[j + 1] = temp
                else:
                    break
        # Start bravada
        print("--------------------------------------------------------------------------------------------------")
        print(self.lang['brav_phase'],"\n")
        for i in range(len(self.battle_chain)):
            self.battle_chain.pop().on()
        #Requiem counters activation
        for creature in self.characters:
            creature.activate_counters(1)
        #Score up all member
        print("--------------------------------------------------------------------------------------------------")
        print(self.lang['res'],"\n")
        for char in self.characters:
            char.score_up()
        print("--------------------------------------------------------------------------------------------------")

        # Start requiem
        #print("Prepare requiem phase: \n")
        current_chain = insert_chain
        self.battle_chain = []
        for i in range(len(requiem_queue)):
            act = requiem_queue.pop()
            current_chain = Creature.try_act(act=act, cur_chain=current_chain,
                                            cur_party=self.characters,
                                            battle_chain=self.battle_chain)
        print(self.lang['req_phase'],"\n")
        for i in range(len(self.battle_chain)):
            self.battle_chain.pop().on()
        #Refresh action counters
        for char in self.characters:
            char.refresh_action_counters()
    def enemys_alive(self):
        teams = []
        count = 0
        for team in self.teams:
            for char in self.characters:
                teams.append(char.team_id)
        return len(list(dict.fromkeys(teams))) > 1
    def generate_random_chain(chain_size):
        res = ''
        for i in range(chain_size):
            res +=str(randint(0,9))
        return res
    def refresh_sum_potential(self):
        for char in self.characters:
            self.sum_potential += char.potential
    def battle(self,rounds= -1,mode=0):
        count = 1
        while(self.enemys_alive() and count != rounds):
            print("-------------------------------------------------------------------------------------------------------")
            print("ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            print("-------------------------------------------------------------------------------------------------------")
            print(self.lang['round'],count,"\n")
            chain = BattleField.generate_random_chain(chain_size= self.sum_potential)
            print("[",chain,"]\n")
            self.turn_round(chain, mode=mode)
            self.sum_potential = 0
            for char in self.characters:
                if(not(char.isAlive())):
                    print("XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX")
                    print(char.name,self.lang['dead'])
                    print("XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX\n")
                    self.characters.remove(char)
                else:
                    self.sum_potential += char.potential
            count +=1
        print(self.lang['b_over'])
        print(self.lang['r_count'], count)
        print(self.lang['winner'], self.characters[0].team_id)






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    prime_lang = Language()
    prime_lang.load_dict("RUS")
    lang = prime_lang.storage
    scene = []
    fallen_one = Creature(name= "Fallen Warrior1", team_id=1, logs=[], tokens= [], potential= 4, lang=lang)
    Protect(sender= fallen_one,mask= "2",mask_size= 1, action_class= 0, lang=lang)
    Attack(sender= fallen_one,mask= "4",mask_size= 1, action_class= 0,lang=lang)

    dummy1 = Creature(name= "Dummy1", team_id=1, logs=[], tokens= [], potential= 6, HP=10,lang=lang)
    Protect(sender=dummy1, mask=r"3", mask_size=2, action_class=0,lang=lang)
    dummy2 = Creature(name="Dummy2", team_id=1, logs=[], tokens=[], potential=6, HP=10,lang=lang)

    ingrid = Creature(name= "Ingrid", team_id=0, logs=[], tokens= [], potential= 6, HP=5,lang=lang)
    Blanked_Spray(sender= ingrid,mask= r"\S*3\S*3\S*3\S*", mask_size= 3, action_class=-1,lang=lang)
    Water_Blast(sender= ingrid,mask= r"1[2468]", mask_size= 2, action_class= 0,lang=lang)
    Froze_Up(sender= ingrid,mask= r"[57]9", mask_size= 2, action_class= 1,lang=lang)

    lary = Creature(name= "Lary", team_id=0, logs=[], tokens= [], potential= 6, HP=5,distant_power= 1,lang=lang)
    Token.increase(owner=lary,token= Arrow_Token, n= 10)
    Legioner_Judge(sender= lary,mask= r"\S*8\S*8\S*8\S*", mask_size= 3, action_class= -1,lang=lang)
    Blinking_Daggers(sender= lary,mask= r"\S*2\S*2\S*2\S*", mask_size= 3, action_class= -1,lang=lang)
    Stab(sender= lary,mask= r"3[13579]", mask_size= 2, action_class= 0,lang=lang)

    fafnir = Creature(name="Fafnir", team_id=0,logs=[], tokens= [], potential=6, HP= 10,attack= 2,lang=lang)
    Group_Up(sender= fafnir,mask= r"\S*3\S*3\S*3\S*", mask_size= 3, action_class= -1,lang=lang)
    Force_Attack(sender= fafnir,mask= r"1[3579]", mask_size= 2, action_class= 0,lang=lang)
    Swing_Slash(sender= fafnir,mask= r"(13)|(31)", mask_size= 2, action_class= 0,lang=lang)

    wolf1 = Creature(name="Wolf1", team_id=1, logs=[], tokens=[], potential=6, HP=5, attack=2,lang=lang)
    Bite(sender=wolf1, mask=r"5", mask_size=1, action_class=0,lang=lang)
    wolf2 = Creature(name="Wolf2", team_id=1, logs=[], tokens=[], potential=6, HP=5, attack=2,lang=lang)
    Bite(sender=wolf2, mask=r"6", mask_size=1, action_class=0,lang=lang)
    wolf3 = Creature(name="Wolf3", team_id=1, logs=[], tokens=[], potential=6, HP=5, attack=2,lang=lang)
    Bite(sender=wolf3, mask=r"7", mask_size=1, action_class=0,lang=lang)

    scene.append(ingrid)
    scene.append(lary)
    scene.append(fafnir)
    scene.append(wolf1)
    scene.append(wolf2)
    scene.append(wolf3)

    encounter = BattleField(scene,lang=lang)
    encounter.battle()
    #encounter.turn_round("98505841320248",mode= 0)
    #player1.show_status()
    #player2.show_status()
    print(lang.items())
    print()


