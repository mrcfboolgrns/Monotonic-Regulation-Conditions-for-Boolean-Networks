from fontTools.misc.textTools import tostr

from BoolNet.Node import *


class RegulationConditions_Optional:
    def __init__(self,c,q,optional):
        self.c=c
        self.sources=c.sources
        self.def_sources = []
        for src in self.sources.keys():
            if self.sources[src][2] != 'True':
                self.def_sources.append(src)
        self.addit_pos = self.addit_neg = ''
        self.q=q
        #self.RegConditions={}
        self.k = 0
        self.optional=optional
        self.def_sources_neg = [src for src in self.def_sources if self.sources[src][0]=='negative']
        self.def_sources_pos = [src for src in self.def_sources if self.sources[src][0] == 'positive']
        self.opt_sources_neg = [src for src in self.optional if src[1]=='negative']
        self.opt_sources_pos = [src for src in self.optional if src[1] == 'positive']
    def NotInducible(self):
        for src in self.sources.values():
            if src[0]=="positive":
                return False
        return True

    def NotRepressible(self):
        for src in self.sources.values():
            if src[0]=="negative":
                return False
        return True

    def AllActivators(self,k):
        str1 = ''
        for opt in self.optional:
            if opt[1]=="positive":
                str1+=f"((edge_{opt[0]}_{self.c.name}_positive) ? {opt[0]}{k} : {self.addit_pos}) & "
        if (len(self.sources.keys())==0):
            str1 = str1[:-3]
        if self.NotInducible():
            return str1

        for src in self.sources.keys():
            if self.sources[src][0]=='positive' and self.sources[src][2]!='True': ########################### [2] with group in [1] place
                str1+=src + str(k)+' & '
        str1 = str1[:-3]
        # for src in self.sources.keys():
        #     if src[1]=='False' and src[0] == 'positive' and  :
        #         return False
        return str1

    def AllRepressors(self,k):
        str1 = ''
        for opt in self.optional:
            if opt[1] == "negative":
                str1 += f"((edge_{opt[0]}_{self.c.name}_negative) ? {opt[0]}{k}: {self.addit_neg}) & "
        if (len(self.sources.keys())==0):
            str1 = str1[:-3]
        if self.NotRepressible():
            return str1

        for src in self.sources.keys():
            if self.sources[src][0] == 'negative'and self.sources[src][2]!='True':###########################
                str1 += src + str(k)+ ' & '
        str1 = str1[:-3]
        # for src in self.sources.keys():
        #     if src[1]=='False' and src[0] == 'positive' and  :
        #         return False
        return str1

    def NoActivators(self,k):
        str1 = ''
        for opt in self.optional:
            if opt[1] == "positive":

                str1 += f"((edge_{opt[0]}_{self.c.name}_positive) ? !{opt[0]}{k}: {self.addit_pos}) & "
        if (len(self.sources.keys())==0):
            str1 = str1[:-3]
        for src in self.sources.keys():
            if self.sources[src][0] =='positive' and self.sources[src][2]!='True':###########################
                str1 += '!'+src+ str(k)+ ' & '
        str1 = str1[:-3]

        return str1

    def NoRepressors(self,k):
        str1 = ''
        for opt in self.optional:
            if opt[1] == "negative":
                str1 += f"((edge_{opt[0]}_{self.c.name}_negative) ? !{opt[0]}{k} : {self.addit_neg}) & "
        if (len(self.sources.keys())==0):
            str1 = str1[:-3]
        for src in self.sources.keys():
            if self.sources[src][0] == 'negative' and self.sources[src][2]!='True':###########################
                str1 += '!' + src+ str(k) + ' & '
        str1 = str1[:-3]
        return str1
    # def NotInducible(self):
    #     # for src in self.def_sources_pos:
    #     #     if src[0] == "positive":
    #     #         return False
    #     # return True
    #
    #
    #     # for src in self.sources.values():
    #     #     if src[0] == "positive":
    #     #         return False
    #     # return True
    #
    #
    #
    #     str1="FALSE"
    #     if self.opt_sources_pos!=[]:
    #         str1="("
    #         for opt in self.opt_sources_pos:
    #             str1+= f"!edge_{opt[0]}_{self.c.name}_positive & "
    #         str1 = str1[:-3]
    #         str1 += f"?FALSE:TRUE)"
    #     if self.def_sources_pos == []:
    #         return str1
    #     else:
    #         return 'TRUE'
    #
    # def NotRepressible(self):
    #     #for src in self.sources.values():
    #       #  if src[0]=="negative":
    #      #       return False
    #     #return True
    #     str1 = "FALSE"
    #     if self.opt_sources_neg != []:
    #         str1 = "("
    #         for opt in self.opt_sources_neg:
    #             str1 += f"!edge_{opt[0]}_{self.c.name}_negative & "
    #         str1 = str1[:-3]
    #         str1 += f"?FALSE:TRUE)"
    #     if self.def_sources_neg == []:
    #         return str1
    #     else:
    #         return 'TRUE'
    #
    # def AllActivators(self,k):
    #
    #     str1 = self.NotInducible() +" & "
    #     for opt in self.optional:
    #         if opt[1]=="positive":
    #             str1+=f"((edge_{opt[0]}_{self.c.name}_positive) ? {opt[0]}{k} : {self.addit_pos}) & "
    #     for src in self.sources.keys():
    #         if self.sources[src][0]=='positive' and self.sources[src][2]!='True': ########################### [2] with group in [1] place
    #             str1+=src + str(k)+' & '
    #     str1 = str1[:-3]
    #     # for src in self.sources.keys():
    #     #     if src[1]=='False' and src[0] == 'positive' and  :
    #     #         return False
    #     return str1
    #     # str1 = ''
    #     # for opt in self.optional:
    #     #     if opt[1]=="positive":
    #     #         str1+=f"((edge_{opt[0]}_{self.c.name}_positive) ? {opt[0]}{k} : {self.addit_pos}) & "
    #     #
    #     # if (len(self.def_sources_pos)==0):
    #     #     str1 = str1[:-3]
    #     # if self.NotInducible():
    #     #     temp=""
    #     #     if self.opt_sources_pos!=[]:
    #     #         if (len(self.def_sources_pos)==0):
    #     #             temp=" & ("
    #     #         else:
    #     #             temp="("
    #     #         for opt in self.optional:
    #     #             if opt[1] == "positive":
    #     #                 temp+= f"!edge_{opt[0]}_{self.c.name}_positive) &"
    #     #         temp=temp[:-3]
    #     #         temp+=f"?FALSE:TRUE)"
    #     #
    #     #     return str1 + temp
    #     #
    #     # for src in self.sources.keys():
    #     #     if self.sources[src][0]=='positive' and self.sources[src][2]!='True': ########################### [2] with group in [1] place
    #     #         str1+=src + str(k)+' & '
    #     # str1 = str1[:-3]
    #     # # for src in self.sources.keys():
    #     # #     if src[1]=='False' and src[0] == 'positive' and  :
    #     # #         return False
    #     # return str1
    #
    # def AllRepressors1(self,k):
    #     str1 = ''
    #     for opt in self.optional:
    #         if opt[1] == "negative":
    #             str1 += f"(!(edge_{opt[0]}_{self.c.name}_negative) ? {opt[0]}{k}: {self.addit_neg}) & "
    #     if (len(self.sources.keys())==0):
    #         str1 = str1[:-3]
    #     if self.NotRepressible():
    #         return str1
    #
    #     for src in self.sources.keys():
    #         if self.sources[src][0] == 'negative'and self.sources[src][2]!='True':###########################
    #             str1 += "!"+src + str(k)+ ' & '
    #     str1 = str1[:-3]
    #     # for src in self.sources.keys():
    #     #     if src[1]=='False' and src[0] == 'positive' and  :
    #     #         return False
    #     return str1
    #
    # def AllRepressors(self,k):
    #     str1 = self.NotRepressible() + " & "
    #     for opt in self.optional:
    #         if opt[1] == "negative":
    #             str1 += f"((edge_{opt[0]}_{self.c.name}_negative) ? {opt[0]}{k} : {self.addit_pos}) & "
    #     for src in self.sources.keys():
    #         if self.sources[src][0] == 'negative' and self.sources[src][2] != 'True':  ########################### [2] with group in [1] place
    #             str1 += src + str(k) + ' & '
    #     str1 = str1[:-3]
    #     # for src in self.sources.keys():
    #     #     if src[1]=='False' and src[0] == 'positive' and  :
    #     #         return False
    #     return str1
    #     # str1 = ''
    #     # for opt in self.optional:
    #     #     if opt[1] == "negative":
    #     #         str1 += f"((edge_{opt[0]}_{self.c.name}_negative) ? {opt[0]}{k}: {self.addit_neg}) & "
    #     # if (len(self.sources.keys())==0):
    #     #     str1 = str1[:-3]
    #     # if self.NotRepressible():
    #     #     return str1
    #     #
    #     # for src in self.sources.keys():
    #     #     if self.sources[src][0] == 'negative'and self.sources[src][2]!='True':###########################
    #     #         str1 += src + str(k)+ ' & '
    #     # str1 = str1[:-3]
    #     # # for src in self.sources.keys():
    #     # #     if src[1]=='False' and src[0] == 'positive' and  :
    #     # #         return False
    #     # return str1
    #
    # def NoActivators(self,k):
    #     str1 = ''
    #     for opt in self.optional:
    #         if opt[1] == "positive":
    #
    #             str1 += f"((edge_{opt[0]}_{self.c.name}_positive) ? !{opt[0]}{k}: {self.addit_pos}) & "
    #     if (len(self.sources.keys())==0):
    #         str1 = str1[:-3]
    #     for src in self.sources.keys():
    #         if self.sources[src][0] =='positive' and self.sources[src][2]!='True':###########################
    #             str1 += '!'+src+ str(k)+ ' & '
    #     str1 = str1[:-3]
    #
    #     return str1
    #
    # def NoRepressors(self,k):
    #     str1 = ''
    #     for opt in self.optional:
    #         if opt[1] == "negative":
    #             str1 += f"((edge_{opt[0]}_{self.c.name}_negative) ? !{opt[0]}{k} : {self.addit_neg}) & "
    #     if (len(self.sources.keys())==0):
    #         str1 = str1[:-3]
    #     for src in self.sources.keys():
    #         if self.sources[src][0] == 'negative' and self.sources[src][2]!='True':###########################
    #             str1 += '!' + src+ str(k) + ' & '
    #     str1 = str1[:-3]
    #     return str1



    def eval_dict(self,k): #create the dictionary for each node with correct synthesis

        dict1 = {}
        self.k = k
        if len(self.def_sources_pos) == 0:
            self.addit_pos = f"{self.c.name + str(k)}"
        else:
            self.addit_pos = 'TRUE'
        if len(self.def_sources_neg) == 0:
            self.addit_neg = f"{self.c.name + str(k)}"
        else:
            self.addit_neg = 'TRUE'

        self.addit_neg = 'TRUE'
        self.addit_pos = 'TRUE'


        AllActivators = self.AllActivators(k)
        AllRepressors = self.AllRepressors(k)
        NoActivators = self.NoActivators(k)
        NoRepressors = self.NoRepressors(k)
        # dict1['R0'] = '((' + self.check_and(str(AllActivators)) + ')&(' + self.check_and(str(NoRepressors)) + '))'
        # dict1['R1'] = '((!(' + self.check_and(str(NoActivators)) + '))&(' + self.check_and(str(NoRepressors)) + '))'
        # dict1['R2'] = '((' + self.check_and(str(AllActivators)) + ')&(!(' + self.check_or(str(AllRepressors)) + ')))'
        # dict1['R3'] = '(((!(' + self.check_or(str(NoActivators)) + '))&(' + self.check_and(str(NoRepressors)) + '))|((' + self.check_or(str(
        #     AllActivators)) + ')&(!(' + self.check_or(str(AllRepressors)) + '))))'
        # dict1['R4'] = '((' + self.check_and(str(AllActivators)) + '))'
        # dict1['R5'] = '((' + self.check_or(str(AllActivators)) + ')|((' + self.check_and(str(NoRepressors)) + ')&(!(' + self.check_or(str(NoActivators)) + '))))'
        # dict1['R6'] = '((!(' + self.check_or(str(NoActivators)) + '))&(!(' + self.check_or(str(AllRepressors)) + ')))'
        # dict1['R7'] = '(((!(' + self.check_or(str(NoActivators)) + '))&(!(' + self.check_or(str(AllRepressors)) + ')))|(' + self.check_or(str(AllActivators)) + '))'
        # dict1['R8'] = '(!(' + self.check_and(str(NoActivators)) + '))'
        # dict1['R9'] = '((' + self.check_and(str(NoRepressors)) + '))'
        # dict1['R10'] = '((' + self.check_or(str(NoRepressors)) + ')|((!(' + self.check_and(str(AllRepressors)) + '))&(' + self.check_and(str(AllActivators)) + ')))'
        # dict1['R11'] = '((' + self.check_or(str(NoRepressors)) + ')|((!(' + self.check_and(str(NoActivators)) + '))&(!(' + self.check_or(str(AllRepressors)) + '))))'
        # dict1['R12'] = '(!(' + self.check_or(str(AllRepressors)) + '))'
        # dict1['R13'] = '((' + self.check_and(str(NoRepressors)) + ')|(' + self.check_and(str(AllActivators)) + '))'
        # dict1['R14'] = '(((' + self.check_and(str(NoRepressors)) + ')|(' + self.check_or(str(AllActivators)) + '))|((!(' + '('+self.check_and(str(
        #     AllRepressors)) + '))&(!(' + self.check_or(str(NoActivators)) + ')))))'
        #dict1['R15'] = '((!(' + self.check_or(str(AllRepressors)) + '))|(' + self.check_and(str(AllActivators)) + '))'
        # dict1['R16'] = '((' + self.check_and(str(NoRepressors)) + ')|(!(' + self.check_or(str(NoActivators)) + ')))'
        # dict1['R17'] = '((!(' + self.check_or(str(AllRepressors)) + '))|(!(' + self.check_or(str(NoActivators)) + ')))'

        dict1['R0'] = '((' + self.check_and(str(AllActivators)) + ')&(' + self.check_and(str(NoRepressors)) + '))'
        dict1['R1'] = '((!(' + self.check_or(str(NoActivators)) + '))&(' + self.check_and(str(NoRepressors)) + '))'
        dict1['R2'] = '((' + self.check_and(str(AllActivators)) + ')&(!(' + self.check_or(str(AllRepressors)) + ')))'
        dict1['R3'] = '(((!(' + self.check_or(str(NoActivators)) + '))&(' + self.check_and(
            str(NoRepressors)) + '))|((' + self.check_or(str(
            AllActivators)) + ')&(!(' + self.check_or(str(AllRepressors)) + '))))'
        dict1['R4'] = '((' + self.check_and(str(AllActivators)) + '))'
        dict1['R5'] = '((' + self.check_or(str(AllActivators)) + ')|((' + self.check_or(
            str(NoRepressors)) + ')&(!(' + self.check_or(str(NoActivators)) + '))))'
        dict1['R6'] = '((!(' + self.check_and(str(NoActivators)) + '))&(!(' + self.check_or(str(AllRepressors)) + ')))'
        dict1['R7'] = '(((!(' + self.check_or(str(NoActivators)) + '))&(!(' + self.check_or(
            str(AllRepressors)) + ')))|(' + self.check_or(str(AllActivators)) + '))'
        dict1['R8'] = '(!(' + self.check_and(str(NoActivators)) + '))'
        dict1['R9'] = '((' + self.check_and(str(NoRepressors)) + '))'
        dict1['R10'] = '((' + self.check_or(str(NoRepressors)) + ')|((!(' + self.check_and(
            str(AllRepressors)) + '))&(' + self.check_and(str(AllActivators)) + ')))'
        dict1['R11'] = '((' + self.check_or(str(NoRepressors)) + ')|((!(' + self.check_or(
            str(NoActivators)) + '))&(!(' + self.check_and(str(AllRepressors)) + '))))'
        dict1['R12'] = '(!(' + self.check_or(str(AllRepressors)) + '))'
        dict1['R13'] = '((' + self.check_or(str(NoRepressors)) + ')|(' + self.check_or(str(AllActivators)) + '))'
        dict1['R14'] = '(((' + self.check_or(str(NoRepressors)) + ')|(' + self.check_or(
            str(AllActivators)) + '))|((!(' + '(' + self.check_or(str(
            AllRepressors)) + '))&(!(' + self.check_or(str(NoActivators)) + ')))))'
        dict1['R15'] = '((!(' + self.check_or(str(AllRepressors)) + '))|(' + self.check_or(str(AllActivators)) + '))'
        dict1['R16'] = '((' + self.check_and(str(NoRepressors)) + ')|(!(' + self.check_and(str(NoActivators)) + ')))'
        dict1['R17'] = '((!(' + self.check_or(str(AllRepressors)) + '))|(!(' + self.check_and(str(NoActivators)) + ')))'

        return dict1


        # dict1['R0'] = '((' + str(AllActivators) + ')&(' + str(NoRepressors) + '))'
        # dict1['R1'] = '((!(' + str(NoActivators) + '))&(' + str(NoRepressors) + '))'
        # dict1['R2'] = '((' + str(AllActivators) + ')&(!(' + str(AllRepressors) + ')))'
        # dict1['R3'] = '(((!(' + str(NoActivators) + '))&(' + str(NoRepressors) + '))|((' + str(
        #     AllActivators) + ')&(!(' + str(AllRepressors) + '))))'
        # dict1['R4'] = '((' + str(AllActivators) + '))'
        # dict1['R5'] = '((' + str(AllActivators) + ')|((' + str(NoRepressors) + ')&(!(' + str(NoActivators) + '))))'
        # dict1['R6'] = '((!(' + str(NoActivators) + '))&(!(' + str(AllRepressors) + ')))'
        # dict1['R7'] = '(((!(' + str(NoActivators) + '))&(!(' + str(AllRepressors) + ')))|(' + str(AllActivators) + '))'
        # dict1['R8'] = '(!(' + str(NoActivators) + '))'
        # dict1['R9'] = '((' + str(NoRepressors) + '))'
        # dict1['R10'] = '((' + str(NoRepressors) + ')|((!(' + str(AllRepressors) + '))&(' + str(AllActivators) + ')))'
        # dict1['R11'] = '((' + str(NoRepressors) + ')|((!(' + str(NoActivators) + '))&(!(' + str(AllRepressors) + '))))'
        # dict1['R12'] = '(!(' + str(AllRepressors) + '))'
        # dict1['R13'] = '((' + str(NoRepressors) + ')&(' + str(AllActivators) + '))'
        # dict1['R14'] = '(((' + str(NoRepressors) + ')&(' + str(AllActivators) + '))|((!(' + str(
        #     AllRepressors) + '))&(!(' + str(NoActivators) + '))))'
        # dict1['R15'] = '((!(' + str(AllRepressors) + '))&(' + str(AllActivators) + '))'
        # dict1['R16'] = '((' + str(NoRepressors) + ')&(!(' + str(NoActivators) + ')))'
        # dict1['R17'] = '((!(' + str(AllRepressors) + '))&(!(' + str(NoActivators) + ')))'

    def check_and(self, str1):
        if str1=='':
            return 'TRUE'
        else:
            return str1
    def check_or(self,str1):
        if str1=='':
            return 'FALSE'
        else:
            return str1
        # def NotInducible(self):
    #     for src in self.sources.values():
    #         if src[0]=="positive":
    #             return False
    #     return True
    #
    # def NotRepressible(self):
    #     for src in self.sources.values():
    #         if src[0]=="negative":
    #             return False
    #     return True
    #
    # def AllActivators(self):
    #     if self.NotInducible():
    #         return False
    #
    #     for src in self.sources.keys():
    #
    #         if self.sources[src][0]=='positive' and self.q[src]=='0':
    #             return False
    #     # for src in self.sources.keys():
    #     #     if src[1]=='False' and src[0] == 'positive' and  :
    #     #         return False
    #     return True
    #
    # def AllRepressors(self):
    #     if self.NotRepressible():
    #         return False
    #     for src in self.sources.keys():
    #         if self.sources[src][0] =='negative' and self.q[src]=='0':
    #             return False
    #     # for src in self.sources.keys():
    #     #     if src[1]=='True':
    #     #         return False
    #     return True
    #
    # def NoActivators(self):
    #     for src in self.sources.keys():
    #         if self.sources[src][0] =='positive' and self.q[src]=='1':
    #             return False
    #     return True
    #
    # def NoRepressors(self):
    #     for src in self.sources.keys():
    #         if self.sources[src][0] == 'negative' and self.q[src] == '1':
    #             return False
    #     return True
    #
    # def eval_dict(self):
    #     dict1 = {}
    #     AllActivators = self.AllActivators()
    #     AllRepressors = self.AllRepressors()
    #     NoActivators = self.NoActivators()
    #     NoRepressors = self.NoRepressors()
    #
    #     dict1['R0'] = AllActivators and NoRepressors
    #     dict1['R1'] = not NoActivators and NoRepressors
    #     dict1['R2'] = AllActivators and not AllRepressors
    #     dict1['R3'] = (not NoActivators and NoRepressors) or (
    #                 AllActivators and not AllRepressors)
    #     dict1['R4'] = AllActivators
    #     dict1['R5'] = AllActivators or (NoRepressors and not NoActivators)
    #     dict1['R6'] = not NoActivators and not AllRepressors
    #     dict1['R7'] = (not NoActivators and not AllRepressors) or AllActivators
    #     dict1['R8'] = not NoActivators
    #     dict1['R9'] = NoRepressors
    #     dict1['R10'] = NoRepressors or (not AllRepressors and AllActivators)
    #     dict1['R11'] = NoRepressors or (not NoActivators and not AllRepressors)
    #     dict1['R12'] = not AllRepressors
    #     dict1['R13'] = NoRepressors and AllActivators
    #     dict1['R14'] = (NoRepressors and AllActivators) or (
    #                 not AllRepressors and not NoActivators)
    #     dict1['R15'] = not AllRepressors and AllActivators
    #     dict1['R16'] = NoRepressors and not NoActivators
    #     dict1['R17'] = not AllRepressors and not NoActivators
    #     return dict1

    #all regulation conditions
    # def R0(self):
    #     return self.AllActivators() and self.NoRepressors()
    # def R1(self):
    #     return not self.NoActivators() and self.NoRepressors()
    # def R2(self):
    #     return self.AllActivators() and not self.AllRepressors()
    # def R3(self):
    #     return (not self.NoActivators() and self.NoRepressors()) or (self.AllActivators() and not self.AllRepressors())
    # def R4(self):
    #     return self.AllActivators()
    # def R5(self):
    #     return self.AllActivators() or (self.NoRepressors() and not self.NoActivators())
    # def R6(self):
    #     return not self.NoActivators() and not self.AllRepressors()
    # def R7(self):
    #     return (not self.NoActivators() and not self.AllRepressors()) or self.AllActivators()
    # def R8(self):
    #     return not self.NoActivators()
    # def R9(self):
    #     return self.NoRepressors()
    # def R10(self):
    #     return self.NoRepressors() or (not self.AllRepressors() and self.AllActivators())
    # def R11(self):
    #     return self.NoRepressors() or (not self.NoActivators() and not self.AllRepressors())
    # def R12(self):
    #     return not self.AllRepressors()
    # def R13(self):
    #     return self.NoRepressors() and self.AllActivators()
    # def R14(self):
    #     return (self.NoRepressors() and self.AllActivators()) or (not self.AllRepressors() and not self.NoActivators())
    # def R15(self):
    #     return not self.AllRepressors() and self.AllActivators()
    # def R16(self):
    #     return self.NoRepressors() and not self.NoActivators()
    # def R17(self):
    #     return not self.AllRepressors() and not self.NoActivators()
