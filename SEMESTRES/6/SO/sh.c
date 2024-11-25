#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>

/* MARK NAME Antônio Caetano Neves Neto */
/* MARK NAME João Lucas Simões Moreira */

/****************************************************************
 * Shell xv6 simplificado
 *
 * Este codigo foi adaptado do codigo do UNIX xv6 e do material do
 * curso de sistemas operacionais do MIT (6.828).
 ***************************************************************/

/*
RELATÓRIO

1. Termo de compromisso

Os membros do grupo afirmam que todo o código desenvolvido para este
trabalho é de autoria própria.  Exceto pelo material listado no item 3
deste relatório, os membros do grupo afirmam não ter copiado
material da Internet nem obtiveram código de terceiros.

2. Membros do grupo e alocação de esforço

Preencha as linhas abaixo com o nome e o e-mail dos integrantes do
grupo.  Substitua XX pela contribuição de cada membro do grupo no
desenvolvimento do trabalho.

Antônio Caetano Neves Neto <antonioneto@dcc.ufmg.br> 50%
João Lucas Simões Moreira <joaomoreira@dcc.ufmg.br> 50%

3. Referências bibliográficas

https://learn.microsoft.com/pt-br/windows-server/administration/windows-commands/chdir
https://www.dca.ufrn.br/~adelardo/cursos/DCA409/node39.html
https://www.dca.ufrn.br/~adelardo/cursos/DCA409/node22.html
https://www.dca.ufrn.br/~adelardo/cursos/DCA409/node70.html

4. Estruturas de dados

As estruturas de dados utilizadas na solução foram as presentes no arquivo original
do trabalho, na qual consiste em sintetizar o comando de terminal passado a partir do seu tipo,
qual o comando e argumentos passados, dividindo em três estruturas principais: execução, 
redirecionamento e uso do pipe.

Os algoritmos se basearam em diversas primitivas. No que tange a execução de comandos, a execvp
substitúi o processo atual por um novo processo, a partir do arquivo de execução e seus argumentos.

Para o redirecionamento, a primitiva dup2 foi utilizada. Primeiramente, é aberto o arquivo antes de
sua execução, para evitar possíveis acessos externos e redirecionar a leitura/escrita do processo a
ser executado pelo execvp ao arquivo de interesse. Tal último fato é o que a primitiva dup2 faz. Após,
há uma chamada recursiva para executar o comando de interesse.

Em relação ao pipe, a primitiva pipe é usada para criar um canal de comunicação entre dois processos,
na qual p[0] é utilizado para leitura e p[1] para escrita. Após isso, o processo é duplicado, no qual 
o processo filho executa o comando a esquerda e escreve no canal de escrita o resultado para o processo
pai possa utilizar como entrada, executando recursivamente os comandos.
*/

#define MAXARGS 10

/* Todos comandos tem um tipo.  Depois de olhar para o tipo do
 * comando, o código converte um *cmd para o tipo específico de
 * comando. */
struct cmd
{
  int type; /* ' ' (exec)
               '|' (pipe)
               '<' or '>' (redirection) */
};

struct execcmd
{
  int type;            // ' '
  char *argv[MAXARGS]; // argumentos do comando a ser exec'utado
};

struct redircmd
{
  int type;        // < ou >
  struct cmd *cmd; // o comando a rodar (ex.: um execcmd)
  char *file;      // o arquivo de entrada ou saída
  int mode;        // o modo no qual o arquivo deve ser aberto
  int fd;          // o número de descritor de arquivo que deve ser usado
};

struct pipecmd
{
  int type;          // |
  struct cmd *left;  // lado esquerdo do pipe
  struct cmd *right; // lado direito do pipe
};

int fork1(void);              // Fork mas fechar se ocorrer erro.
struct cmd *parsecmd(char *); // Processar o linha de comando.

/* Executar comando cmd.  Nunca retorna. */
void runcmd(struct cmd *cmd)
{
  int p[2], r;
  struct execcmd *ecmd;
  struct pipecmd *pcmd;
  struct redircmd *rcmd;

  if (cmd == 0)
    exit(0);

  switch (cmd->type){
    default:
      fprintf(stderr, "tipo de comando desconhecido\n");
      exit(-1);

    //ls, cat, rm, sort, uniq, wc
    case ' ':
      ecmd = (struct execcmd *)cmd;
      if (ecmd->argv[0] == 0)
        exit(0);
      /* MARK START task2
      * TAREFA2: Implemente codigo abaixo para executar
      * comandos simples. */
      char* command = ecmd->argv[0];
      execvp(command, ecmd->argv);
      break;

    case '<':
    case '>':
      rcmd = (struct redircmd *)cmd;
      ecmd = (struct execcmd *)cmd;
      /* MARK START task3
      * TAREFA3: Implemente codigo abaixo para executar
      * comando com redirecionamento. */
      r = open(rcmd->file, rcmd->mode, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
      dup2(r, rcmd->fd);
      runcmd(rcmd->cmd);
      /* MARK END task3 */
      break;

    case '|':
      pcmd = (struct pipecmd *)cmd;
      
      /* MARK START task4
      * TAREFA4: Implemente codigo abaixo para executar
      * comando com pipes. */
      pipe(p);
      if (fork1() == 0){
        close(p[0]);
        dup2(p[1], STDOUT_FILENO);
        runcmd(pcmd->left);
      }
      else{
        close(p[1]);
        dup2(p[0], STDIN_FILENO);
        runcmd(pcmd->right);
      }
      /* MARK END task4 */
      break;
    }
    exit(0);
}

int getcmd(char *buf, int nbuf){
  if (isatty(fileno(stdin)))
    fprintf(stdout, "$ ");
  memset(buf, 0, nbuf);
  fgets(buf, nbuf, stdin);
  if (buf[0] == 0) // EOF
    return -1;
  return 0;
}

int main(void){
  static char buf[100];
  int r;

  // Ler e rodar comandos.
  while (getcmd(buf, sizeof(buf)) >= 0)  {
    /* MARK START task1 */
    /* TAREFA1: O que faz o if abaixo e por que ele é necessário?
     * Insira sua resposta no código e modifique o fprintf abaixo
     * para reportar o erro corretamente. */

    /*
      O if abaixo verifica se é o comando 'cd' e verifica se o diretório passado
      como argumento é válido. Caso seja, o diretório atual será alterado. Caso não seja,
      nada acontece.
    */
    // printf("%s\n", buf);
    if (buf[0] == 'c' && buf[1] == 'd' && buf[2] == ' ')    {
      buf[strlen(buf) - 1] = 0;
      if (chdir(buf + 3) < 0)
        fprintf(stderr, "Diretório inexistente.\n");
      continue;
    }
    /* MARK END task1 */

    if (fork1() == 0)
      runcmd(parsecmd(buf));
    wait(&r);
  }
  exit(0);
}

int fork1(void){
  int pid;

  pid = fork();
  if (pid == -1)
    perror("fork");
  return pid;
}

/****************************************************************
 * Funcoes auxiliares para criar estruturas de comando
 ***************************************************************/

struct cmd * execcmd(void){
  struct execcmd *cmd;

  cmd = malloc(sizeof(*cmd));
  memset(cmd, 0, sizeof(*cmd));
  cmd->type = ' ';
  return (struct cmd *)cmd;
}

struct cmd *redircmd(struct cmd *subcmd, char *file, int type){
  struct redircmd *cmd;

  cmd = malloc(sizeof(*cmd));
  memset(cmd, 0, sizeof(*cmd));
  cmd->type = type;
  cmd->cmd = subcmd;
  cmd->file = file;
  cmd->mode = (type == '<') ? O_RDONLY : O_WRONLY | O_CREAT | O_TRUNC;
  cmd->fd = (type == '<') ? 0 : 1;
  return (struct cmd *)cmd;
}

struct cmd *pipecmd(struct cmd *left, struct cmd *right){
  struct pipecmd *cmd;

  cmd = malloc(sizeof(*cmd));
  memset(cmd, 0, sizeof(*cmd));
  cmd->type = '|';
  cmd->left = left;
  cmd->right = right;
  return (struct cmd *)cmd;
}

/****************************************************************
 * Processamento da linha de comando
 ***************************************************************/

char whitespace[] = " \t\r\n\v";
char symbols[] = "<|>";

int gettoken(char **ps, char *es, char **q, char **eq){
  char *s;
  int ret;

  s = *ps;
  while (s < es && strchr(whitespace, *s))
    s++;
  if (q)
    *q = s;
  ret = *s;
  switch (*s)  {
    case 0:
      break;
    case '|':
    case '<':
      s++;
      break;
    case '>':
      s++;
      break;
    default:
      ret = 'a';
      while (s < es && !strchr(whitespace, *s) && !strchr(symbols, *s))
        s++;
      break;
  }
  if (eq)
    *eq = s;

  while (s < es && strchr(whitespace, *s))
    s++;
  *ps = s;
  return ret;
}

int peek(char **ps, char *es, char *toks)
{
  char *s;

  s = *ps;
  while (s < es && strchr(whitespace, *s))
    s++;
  *ps = s;
  return *s && strchr(toks, *s);
}

struct cmd *parseline(char **, char *);
struct cmd *parsepipe(char **, char *);
struct cmd *parseexec(char **, char *);

/* Copiar os caracteres no buffer de entrada, comeando de s ate es.
 * Colocar terminador zero no final para obter um string valido. */
char *mkcopy(char *s, char *es)
{
  int n = es - s;
  char *c = malloc(n + 1);
  assert(c);
  strncpy(c, s, n);
  c[n] = 0;
  return c;
}

struct cmd *
parsecmd(char *s)
{
  char *es;
  struct cmd *cmd;

  es = s + strlen(s);
  cmd = parseline(&s, es);
  peek(&s, es, "");
  if (s != es)
  {
    fprintf(stderr, "leftovers: %s\n", s);
    exit(-1);
  }
  return cmd;
}

struct cmd *
parseline(char **ps, char *es)
{
  struct cmd *cmd;
  cmd = parsepipe(ps, es);
  return cmd;
}

struct cmd *
parsepipe(char **ps, char *es)
{
  struct cmd *cmd;

  cmd = parseexec(ps, es);
  if (peek(ps, es, "|"))
  {
    gettoken(ps, es, 0, 0);
    cmd = pipecmd(cmd, parsepipe(ps, es));
  }
  return cmd;
}

struct cmd *
parseredirs(struct cmd *cmd, char **ps, char *es)
{
  int tok;
  char *q, *eq;

  while (peek(ps, es, "<>"))
  {
    tok = gettoken(ps, es, 0, 0);
    if (gettoken(ps, es, &q, &eq) != 'a')
    {
      fprintf(stderr, "missing file for redirection\n");
      exit(-1);
    }
    switch (tok)
    {
    case '<':
      cmd = redircmd(cmd, mkcopy(q, eq), '<');
      break;
    case '>':
      cmd = redircmd(cmd, mkcopy(q, eq), '>');
      break;
    }
  }
  return cmd;
}

struct cmd *parseexec(char **ps, char *es){
  char *q, *eq;
  int tok, argc;
  struct execcmd *cmd;
  struct cmd *ret;

  ret = execcmd();
  cmd = (struct execcmd *)ret;

  argc = 0;
  ret = parseredirs(ret, ps, es);
  while (!peek(ps, es, "|"))
  {
    if ((tok = gettoken(ps, es, &q, &eq)) == 0)
      break;
    if (tok != 'a')
    {
      fprintf(stderr, "syntax error\n");
      exit(-1);
    }
    cmd->argv[argc] = mkcopy(q, eq);
    argc++;
    if (argc >= MAXARGS)
    {
      fprintf(stderr, "too many args\n");
      exit(-1);
    }
    ret = parseredirs(ret, ps, es);
  }
  cmd->argv[argc] = 0;
  return ret;
}

// vim: expandtab:ts=2:sw=2:sts=2
