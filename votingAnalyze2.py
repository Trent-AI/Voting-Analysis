
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
f = open("US_Senate_voting_data_109.txt") 
records = list(f) #full list of voting records

# list of indexes for each party
class voteAnalysis:
    def __init__(self,file):
        f = open("US_Senate_voting_data_109.txt") 
        self.records, self.df = self.processVotes(list(f))        

    def processVotes(self,records, cols=["Name","Party","State"], party={'D' : [],'R' : []} ):
        names = []
        for i in range(46):
            cols.append("p"+str(i))
        
        for i in range(len(records)):
            records[i] = records[i].split(" ")
            records[i][-1] = records[i][-1][:len(records[i][-1])-1]
            names.append(records[i][0])
            
        for r in range(len(records)): 
            for c in range(len(records[r])-3):
                records[r][c+3] = int(records[r][c+3])
        return records,  pd.DataFrame(records, columns = cols, index = names)
    
        
        self.vote_records = self.df[list(self.df[list(self.df.columns)[3:]])]
    
    def policy_compare(self,s1,s2,array = False):
        votes1 = np.array(self.df.loc[s1][3:])
        votes2 = np.array(self.df.loc[s2][3:])
        return votes1.dot(votes2.T)
        
    def most_similar(self,senator):
        if self.df.Name[0] == senator:
            most = self.policy_compare(senator, self.df.Name[1])
            msen = self.df.Name[1]
        else:
            most = self.policy_compare(senator, self.df.Name[0])
            msen = self.df.Name[0]
            
        if senator in self.df.Name:
            for name in self.df.Name:
                if not name == senator and most < self.policy_compare(senator,name):
                    most = self.policy_compare(senator,name)
                    msen = name
            return msen
        return False
    
    def least_similar(self, senator):
        if self.df.Name[0] == senator:
            least = self.policy_compare(senator, self.df.Name[1])
            lsen = self.df.Name[1]
        else:
            least = self.policy_compare(senator, self.df.Name[0])
            lsen = self.df.Name[0]
            
        if senator in self.df.Name:
            for name in self.df.Name:
                if not name == senator and least > self.policy_compare(senator,name):
                    least = self.policy_compare(senator,name)
                    lsen = name
            return lsen
        return False
                    
    def compareto_group(self, senator, group):
        group_votes = np.zeros((46,))
        for name in group:
            b = self.df[list(self.df.columns)[3:]].loc[name]
            #print(b)
            group_votes += np.array(b)
        return np.array(self.df.loc[senator][3:]).dot(group_votes.T)
    
    def senate_to_parties(self, party=['D','R'],img='test.png'):
        group = []
        if len(party) > 1:
            compar = list(self.df.Name)
        else:
            compar = list(self.df[self.df.Party==party[0]].Name)
        for name in self.df[self.df.Party == "R"].Name:
            group.append(self.compareto_group(name,compar))
        for name in self.df[self.df.Party == "D"].Name:
            group.append(self.compareto_group(name,compar))
        if party == ['D']:
            title = 'Democratic'
        elif party == ['R']:
            title = 'Republican'
        else:
            title = 'Average'
        matplotlib.rc('xtick', labelsize=75) 
        matplotlib.rc('ytick', labelsize=75)
        plt.figure(figsize=(100,60))
        plt.ylim((0,max([2250,max(group)+100])))
        print(max(group))
        plt.rcParams.update({'font.size': 120})
        plt.title("How "+title+" is a Senator")
        plt.xlabel("Senator")
        plt.ylabel("Similarity to "+title+" Senators")
        print(len(group))
        barlist = plt.bar(range(len(group)),group)
        for i in range(len(group)):
            if i < len(self.df[self.df.Party == 'R']):
                barlist[i].set_color('r')
            else:
                barlist[i].set_color('b')  
        plt.savefig(img)
        plt.show()
        

vote = voteAnalysis(f)                   
