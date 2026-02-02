import lizard
#from git import Repo

import pandas as pd
from datetime import datetime
from github import Github, Auth


org="Bradesco-Core"

TOKEN= toke-git


auth = Auth.Token(TOKEN)
g = Github(auth=auth)

user = g.get_user()
print(user.login)


projeto = pd.DataFrame(columns=[ 'Repository', 'Branch',  'arquivos'])
arquivos = pd.DataFrame(columns=['Arquivo', 'Método', 'Complexidade', 'Linhas'])
projeto_list = []
arquivo_list = []


print("Iniciando busca nos repositorios da organizacao: " + org)
print ("Tamanho da organizacao: " + str(g.get_user().get_repos().totalCount) + " repositorios encontrados. ")
 
if(g.get_user().get_repos().totalCount<=0):
    print("Nenhum repositorio encontrado. Verifique o token de acesso. ")
    exit()

for repo in g.get_user().get_repos():#g.get_organization(org).get_repos():

     #if(repo.name.find("ochb-srv")>=0 and repo.name.find("srv")>0):

       print ("================================================================ ")     
       print("Procurando no repositorio: " + repo.name)
       print ("================================================================ ")     
 
       # List all branches
       branches = repo.get_branches()

       for branch in branches:
           
           if branch.name.find("develop")>=0:
                           
              file = repo.get_contents("", ref=branch.name)
              while file:
                  content_file = file.pop(0)
                  if content_file.type == "dir":
                      file.extend(repo.get_contents(content_file.path, ref=branch.name))
                  else:
                      if content_file.name.endswith(".java") and content_file.name.find("Test")<0 and content_file.name.find("Enum")<0:
                          file_content = content_file.decoded_content.decode("utf-8")
                          analysis = lizard.analyze_file.analyze_source_code(content_file.path, file_content)
                    
                          for function in analysis.function_list:
                              if function.cyclomatic_complexity >10 or function.nloc>50:
                                arquivo_list.append({'Arquivo': content_file.path, 'Método': function.name, 'Complexidade': function.cyclomatic_complexity, 'Linhas': function.nloc})
                              else:
                                 print(f"Arquivo: {content_file.path} | Método: {function.name} | Complexidade: {function.cyclomatic_complexity} | Linhas: {function.NLOC}  ")   
              dfArquivos = pd.DataFrame(arquivo_list)

              projeto_list.append({'Repository': repo.name, 'Branch': branch.name, 'arquivos': dfArquivos.to_dict('records')})

              # Reset for next branch
              arquivo_list = []

print("======= RELATÓRIO FINAL =======" )

df = pd.DataFrame(projeto_list)
df_final = df.explode('arquivos').reset_index(drop=True)
df_final = pd.concat([df_final.drop(['arquivos'], axis=1), 
                     pd.json_normalize(df_final['arquivos'])], axis=1)

print(df_final)      
if(df_final.shape[0]>0):
    df_final.to_excel('resultados_analise_codigo_github-' + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + '.xlsx', index=False)
