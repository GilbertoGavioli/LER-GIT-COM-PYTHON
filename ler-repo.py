#from git import Repo

import pandas as pd
from datetime import datetime
from github import Github, Auth


org= NOME DA ORGANIZACAO ORG

TOKEN=--GERAR UM TOKEN NO GIT E COLOCAR AQUI

#response = requests.get(repo_api_url)

auth = Auth.Token(TOKEN)
g = Github(auth=auth)
contRepos = 0

user = g.get_user()
print(user.login)


mydata = pd.DataFrame(columns=['Owner', 'Repository', 'Branch', 'FileName', 'FilePath'])
data_list = []

print("Iniciando busca nos repositorios da organizacao: " + org)
print ("Tamanho da organizacao: " + str(g.get_user().get_repos().totalCount) + " repositorios encontrados. ")
 
if(g.get_user().get_repos().totalCount<=0):
    print("Nenhum repositorio encontrado. Verifique o token de acesso. ")
    exit()

for repo in g.get_user().get_repos():#g.get_organization(org).get_repos():

       contRepos +=1
     #if(repo.name.find("ochb-srv-cred-capital-giro")>=0 and repo.name.find("srv")>0):

       print ("================================================================ ")     
       print("Procurando no repositorio: " + repo.name)
       print ("================================================================ ")     
 
       # List all branches
       branches = repo.get_branches()

       for branch in branches:
                                         
                results = g.search_code(query='Feing in:file repo:' + org + '/' + repo.name)

                for result in results:

                   if(g.search_code(query='HandleInvalidPublicCertificate in:file repo:' + org + '/' + repo.name).totalCount)<=0:

                      data_list.append({'Owner': repo.owner.login, 'Repository': repo.name, 'Branch': branch.name, 'FileName': result.name, 'FilePath': result.path})


df = pd.DataFrame(data_list)
# Remove duplicates based on 'FileName'
df.drop_duplicates(subset=['FileName'], keep='first', inplace=True)
#print(df)

print("Total de repositorios analisados: " + str(contRepos))
print("Exportando resultados para Excel... ")
if(df.shape[0]>0):
    df.to_excel('resultados_github-' + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + '.xlsx', index=False)
else:
    print("Nenhum resultado encontrado.")    

