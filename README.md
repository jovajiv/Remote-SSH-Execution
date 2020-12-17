# Remote-SSH-Execution
Given a ip/hostname , user , pass , command list  .

executes the command list on the remote host , including error handling and exit status



usage example : 


SSH_Func('x.x.x.x',username,password,[touch ~/empty.txt , dos2unix ~/empty.txt , chmod  +x ~/empty.txt])
