from main import *
import re
import random
import codecs

class Action:
    def __init__(self, sender,mask,mask_size,action_class,lang,counter= 0):
        self.sender = sender
        self.mask = mask
        self.mask_size = mask_size
        self.action_class = action_class
        self.counter = counter
        self.lang = lang
        sender.actions.append(self)
        sorted(sender.actions, key=cmp_to_key(lambda action1, action2: action2.mask_size - action1.mask_size))
    def set_new_mask(self,mask,mask_size):
        self.mask = mask
        self.mask_size = mask_size
    def choose_random_enemy_target(self, targets,mode=0):
        enemies = []
        for creature in targets:
            #Filter friend out of enemies
            if(creature.team_id != self.sender.team_id):
                enemies.append(creature)
                #Increase chance to be choosen, depenced on Revenge Counter value
                for counter in creature.tokens:
                    if(type(counter) == Revenge_Token):
                        for i in range(counter.value):
                            enemies.append(creature)
        #Choose enemy for attack
        if(mode == 0):
            return random.choice(enemies)
        else:
            print(lang['ch_tar'],len(enemies),": ")
            for i in range(len(enemies)):
                print(i+1,"-",enemies[i].name)
            return enemies[int(input())-1]
    def choose_all_enemy_targets(self,targets):
        enemies = []
        for creature in targets:
            # Filter friend out of enemies
            if (creature.team_id != self.sender.team_id):
                enemies.append(creature)
                # Increase chance to be choosen, depenced on Revenge Counter value
                for counter in creature.tokens:
                    if (type(counter) == Revenge_Token):
                        for i in range(counter.value):
                            enemies.append(creature)
        # Choose enemy for attack
        return enemies
    def choose_random_target_by_counter(self, targets, counter_type):
        res = []
        for creature in targets:
            # Filter friend out of enemies
            for counter in creature.tokens:
                if(isinstance(counter,counter_type)):
                    res.append(creature)
        # Choose enemy for attack
        return random.choice(res)
    def choose_random_fellow_target(self,owner, targets):
        fellows = []
        for creature in targets:
            # Filter friend out of enemies
            if (creature.team_id == self.sender.team_id and creature.team_id != owner.team_id):
                fellows.append(creature)
        return random.choice(fellows)
    def choose_all_fellow_targets(self,owner, targets):
        fellows = []
        for creature in targets:
            # Filter friend out of enemies
            if (creature.team_id == self.sender.team_id and creature != owner):
                fellows.append(creature)
        return fellows
    def choose_weakest_enemy_tagret(self, targets):
        enemies = []
        for creature in targets:
            #Filter friend out of enemies
            if(creature.team_id != self.sender.team_id):
                enemies.append(creature)
                #Increase chance to be choosen, depenced on Revenge Counter value
                for counter in creature.tokens:
                    if(type(counter) == Revenge_Token):
                        for i in range(counter.value):
                            enemies.append(creature)
        #Choose enemy for attack
        weakest = enemies[0]
        for creature in enemies:
            if(creature.cur_HP < weakest.cur_HP):
                weakest = creature
        return weakest
    def choose_strongest_enemy_tagret(self, targets):
        enemies = []
        for creature in targets:
            #Filter friend out of enemies
            if(creature.team_id != self.sender.team_id):
                enemies.append(creature)
                #Increase chance to be choosen, depenced on Revenge Counter value
                for counter in creature.tokens:
                    if(type(counter) == Revenge_Token):
                        for i in range(counter.value):
                            enemies.append(creature)
        #Choose enemy for attack
        strongest = enemies[0]
        for creature in enemies:
            if(creature.cur_HP > strongest.cur_HP):
                strongest = creature
        return strongest
    def refresh_counter(self):
        self.counter = 0
    def say_hi(self):
        return str(type(self)) + self.sender.name

class Token:
    def __init__(self,value,status, owner, lang):
        self.value = value
        self.status = status
        self.owner = owner
        self.lang = lang
    def say_hi(self):
        print(str(type(self)), "value ", self.value)
    def increase(owner,token,n= 1, sender= None):
        if(owner.find_token(token) != None):
            owner.find_token(token).increase(val= n)
            print(owner.name, ":", owner.find_token(token).value - n, "->",
                  owner.find_token(token).value, owner.find_token(token).name(),"\n")
        else:
            tok = eval(token.__name__)
            owner.tokens.append(tok(value= n,owner= sender, lang=owner.lang))
            print(owner.name, ": 0 ->",
                  owner.find_token(token).value, owner.find_token(token).name(), "\n")
class Revenge_Token(Token):
    def __init__(self,value,owner, lang):
        super(Revenge_Token, self).__init__(value=value, status=1, owner= owner, lang=lang)
    def name(self):
        return self.lang['revenge_token']
    def release(self, val= 1):
        self.value = 0
    def increase(self,n=1):
        self.value +=n
    def create_revenge_field(characters,lang):
        for character in characters:
            for stranger in characters:
                if(character.team_id != stranger.team_id):
                    character.tokens.append(Revenge_Token(owner= stranger, value= 0,lang=lang))
class Fulfillment_Token(Token):
    def __init__(self,value,owner,lang):
        super(Fulfillment_Token, self).__init__(value=value, status=0, owner= owner, lang= lang)
    def name(self):
        return self.lang['fullfillment_token']
    def release(self, val= 1):
        self.value -= val
    def release_all(self):
        self.value = 0
    def increase(self, val=1):
        self.value += val
class Stun_Token(Token):
    def __init__(self,value, owner, lang):
        Token.__init__(self, value=value, status=1, owner= owner, lang= lang)
    def name(self):
        return self.lang['stun_token']
    def release(self, val= 1):
        if(self.value - val >= 0):
            self.value -= val
        else:
            self.value = 0
    def increase(self, val=1):
        self.value += val
class Arrow_Token(Token):
    def __init__(self,value,owner,lang):
        super(Arrow_Token, self).__init__(value=value, status=0, owner= owner,lang= lang)
    def name(self):
        return self.lang["arrow_token"]
    def release(self, val= 1):
        self.value -= val
    def increase(self, val=1):
        self.value += val
class Bleedness_Token(Token):
    def __init__(self,value,owner,lang):
        super(Bleedness_Token, self).__init__(value=value, status=1, owner= owner,lang= lang)
    def name(self):
        return self.lang['bleedness_token']
    def release(self, val= 1):
        print(self.owner.name,self.lang['bleedness_token_1'])
        print(self.owner.name,":",self.owner.pure_damage,"->",self.owner.pure_damage + self.value,self.lang['p_d'])
        self.owner.pure_damage += self.value
        self.value -= val
    def increase(self, val=1):
        self.value += val

class Creature:
    def __init__(self, lang,HP = 10, attack = 1, protect = 1, shield = 0, name = "Unknown", team_id = 0, tokens = [], logs = [], cur_initiative= 0, potential= 3, distant_power= 0):
        self.name = name
        self.attack_power = attack
        self.protect_power = protect
        self.distant_power = distant_power
        self.max_HP = HP
        self.cur_HP = HP
        self.personal_log = logs
        self.actions = []
        self.team_id = team_id
        self.tokens = tokens
        self.physic_damage = 0
        self.pure_damage = 0
        self.distant_damage = 0
        self.cur_shield = shield
        self.cur_distant_shield = 0
        self.cur_initiative = cur_initiative
        self.potential = potential
        self.lang = lang
        #Base tokens
        self.tokens.append(Stun_Token(value= 0, owner= self,lang = lang))
    def show_logs(self):
        for message in self.personal_log:
            print(message)
    def try_act(act,cur_chain,cur_party,battle_chain):
        chain = cur_chain
        if(re.findall(act.mask,cur_chain) != []):
            for c in range(len(re.findall(act.mask,cur_chain))):
                chain = act.insert(chain=chain,targets=cur_party,battle_chain= battle_chain)
        return chain
    def find_action(self,type):
        for action in self.actions:
            if(isinstance(action,type)):
                return action
        return None
    def find_token(self, type):
        for counter in self.tokens:
            if(isinstance(counter,type)):
                return counter
        return None
    def activate_counters(self,status):
        for counter in self.tokens:
            if(counter.status == status):
                counter.release()
    def score_up(self):
        h = self.cur_HP
        if (self.physic_damage - self.cur_shield  > 0):
            self.pure_damage +=self.physic_damage - self.cur_shield
        if (self.distant_damage - self.cur_distant_shield > 0):
            self.pure_damage +=self.distant_damage - self.cur_distant_shield
        self.cur_HP -= self.pure_damage
        self.step_up()
        if(h != self.cur_HP):
            print(self.name,":",h,"->",self.cur_HP,"HP")
    def show_status(self):
        print(self.lang['name'], self.name)
        print('HP: ', self.cur_HP)
        print(self.lang['shields'], self.cur_shield)
        print()
    def add_message(self,mess):
        self.personal_log.append(mess)
    def step_up(self):
        self.cur_shield = 0
        self.cur_distant_shield
        self.physic_damage = 0
        self.pure_damage = 0
        self.distant_damage = 0
    def isAlive(self):
        return self.cur_HP > 0
    def refresh_action_counters(self):
        for act in self.actions:
            act.refresh_counter()

class Language:
    def __init__(self):
        self.lang = ["ENG","RUS"]
        self.storage = {}
    def load_dict(self,lang):
        if (lang in self.lang):
            dict_file = codecs.open(lang+".txt",'r',"utf-8")
            for line in dict_file.readlines():
                if line[0] == "#" or line == '\n' or line == '\r\n':
                    continue
                val_key = line[:-2].split(" : ")
                self.storage.update({val_key[0]:val_key[1]})
    def show_dict(self):
        for elem in self.storage.items():
            print(elem)
