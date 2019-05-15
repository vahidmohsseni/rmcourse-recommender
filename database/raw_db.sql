DROP TABLE IF EXISTS `sqlite_sequence`;
CREATE TABLE sqlite_sequence(name,seq);
DROP TABLE IF EXISTS `questions`;
CREATE TABLE "questions"(     "id" Integer PRIMARY KEY  NOT NULL  ,      "stack_id" Integer  NOT NULL  ,      "ans_id" Integer  NOT NULL  ,      "ans_tags" Text  NOT NULL  ,      "q_tags" Text  NOT NULL  );
INSERT INTO questions VALUES (1, 218384, 27439, 'java,design-patterns,maven-plugin,excel-vba,jquery,php,types,mercurial,javascript,linux,haskell,.net,mysql,oop,list,animation,sql,calendar,jquery-ui,excel-2007,sql-server,multithreading,datepicker,user-interface,html,jsp,netbeans,arrays,swing,hibernate,class,toggle,web-services,c#,excel,algorithm,bigdecimal,netbeans-7,syntax,jbutton,database,definition,vba,struts2,css,thread-safety,servlets,file,jdbc,maven-2,interface,string,', 'java,nullpointerexception,');
DROP TABLE IF EXISTS `worker`;
CREATE TABLE "worker"(     "id" Integer PRIMARY KEY  NOT NULL  ,      "stack_id" Integer  NOT NULL  ,      "tags" Text  NOT NULL  );
