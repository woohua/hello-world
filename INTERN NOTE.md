# INTERN NOTE

## 企业级应用开发
* 项目和产品的区别：应用只为一个客户开发的为项目，应用开发出来卖给很多客户的为产品

* 项目开发流程：需求分析->设计->数据库设计->表设计->管理

* 数据库设计:考虑到多数据库的支持，权衡使用一些高级功能带来的好处和对可移植性方面带来的损害;在应用架构设计时，使用较好的框架去屏蔽不同数据库的差异，比如J2EE的Hibernate框架等。

* 表设计：原子性优化，查询速度优化，并发性优化，空值字段控制，分页分表，表存储方式、结构

* 管理：代码托管，代码审查，任务发放跟踪，软件测试，版本管理发布部署维护

* 后端开发框架：前端->中间件（中台）->服务->函数>原子服务->原子函数->原子过程

* 业务逻辑->函数封装->数据库，底层代码


## Oracle

*   ### 过程参数传递
    > * IN     实参赋值给形参后，在过程中只读，不可更改   
    > * OUT    不接受实参赋值，初始为NULL，可读写并可传值到过程外
    > * IN OUT  形参接受实参，可读写并可传值到过程外

*   ### rowid 和 rownum 以及分页
    > *   rownum 为查询结果集中的逻辑标志，在不同的 SQL 中不同，当查询返回一条记录则增加1，初始值为1，如果在 where 中对 rownum 进行等值判断`where rownum = 3`,则不会返回任何结果集，因为只有当记录返回的时候 rownum 才会增大，故在此类SQL中不会返回记录 
    > *  rowid为查询结果记录的唯一物理标志，
    > *  rownum 在 where 字句中限定某个字段的范围可以实现分页查询，提高效率

*   ### 执行计划
    >  *  将SQL解释成数据库的底层操作，用于检查SQL的执行效率和各项执行参数，查询优化分析工具

*   ###NULL的一些注意
    > *  Oracle中把空的字符串当作NULL，即`var = ''`和`var <> ''`等价于`var = NULL`和`var <> NULL`， 而以上几种表达式的返回值均为NULL
    > *  `isnull(var)`当var为空时返回0，不为空时返回1

*   ###HINT方法优化查询
    > *  /* +ALL_ROWS*/表明对语句块选择基于开销的优化方法,并获得最佳吞吐量,使资源消耗最小化.例如:　
`SELECT /*+ALL+_ROWS*/ EMP_NO,EMP_NAM,DAT_IN
 FROM BSEMPMS WHERE EMP_NO=’SCOTT’`
    > *  /* +FIRST_ROWS*/表明对语句块选择基于开销的优化方法,并获得最佳响应时间,使资源消耗最小化.例如:
`SELECT /*+FIRST_ROWS*/ EMP_NO,EMP_NAM,DAT_IN 
FROM BSEMPMS WHERE EMP_NO=’SCOTT’`;

*   ###Oracle 字符串操作函数
    > *  `replace(s1,s2,s3)`将s1中的s2替换成s3
    > *  `instr(s1,s2)`     返回s2在s1中的开始位置，首位为1
    > *  `substr(s1,n1,n2)`返回s1中的n1位置开始截取n2长度的字符串
    > *  `trim(s)`      返回去掉前后空格的字符串s
    > *  `lpad(s,l,c)`  以字符c左补齐s至长度l
    > *  `rpad(s,l,c)`  以字符c右补齐s至长度l
    > *  `right(s,l)`   返回s右起l长度的字符串
    > *  `left(s,l)`    返回s左起l长度的字符串

*   ###Oracle 数字操作函数
    > *  `floor(2345.67)` 取整返回  [size=1.1em]2345
    > *  `ceil(3.1415)`   取大于或等于的最小整数 4
    > *  `round(3.1415926,4)` 按给定精度四舍五入 3.1415
    >   `trunc(234,12213435,4)` 按给定精度截取数字不进行    四舍五入 3.1415
    >__区别在于round是四舍五入，trunc是按字符长度截取__

*   ###Oracle 日期操作注意
    > *  __`to_char(sysdate,'yyyy-MM.dd:hh[mi"ss')`__
    >   __报错__ yyyy--mm--dd hh:mm:ss这里分钟和月份冲突
    >   __正确__ yyyy--mm--dd hh:__mi__:ss
    >   24小时：yyyy--mm--dd hh24:mmi:ss
    >   __报错__ `to_char(to_date('232323','hh'),'hh')`时间为  23:23:23,to_date里要用`hh24`，to_char中`hh`可以得到12小时制的时位，`hh24`得到24小时制的时位

*  ### 表空间和表*
    > *  字段默认值，空值
    > *  表空间->段->盘区->数据块
         Tablespace->Segment->Extend->Block
    > *  storage参数
        *  本地管理数据库
            * INITIAL, NEXT 初始化区段大小
            * PCTINCREASE,MINEXTENTS 字段物理存储大小
        *  字典管理数据库
            * MAXEXTENTS  段总长
            * MAXSIZE     存储单元大小
            * FREELISTS   自由列表（改善实时系统段的插入）
            * FREELIST GROUPS  改善空间分配和释放，避免段元数据    跨实例传输

*  ###PL/SQL特殊结构
    > *  %TYPE  `字段名%type`声明变量为特定字段类型
    > *  %ROWTYPE   `表名%rowtype`声明变量为表记录类型
    > *  varray     `varrar(5)`声明变量为有序数组类型   
        数组中的元素使用前必须在declare中初始化，或者使用extend() 
>   * declare
a int_array := int_array(null); 
begin  
  a(1) := 3;
  a.extend();
  a(2) := 4;
  a.extend();
  a(3) := 5;`
 
*  ### 数据处理方式
    *  OLTP(on-line transaction processing)联机事务处理，实时系统（金融业）
    *  OLAP(On-Line Analytical Processing)联机分析处理，分析决策（企业内部）
    
*  ###ROLLBACK用法
    * 直接使用回滚本次事务
    * 回滚至savepoint
    >  insert into t values(1);
       savepoint sp_1;
       insert into t values(2);
       savepoint sp_2;
       insert into t values(3)
       rollback to sp_2;
       前两条插入不会撤销 

*  ###异常
    * 系统异常
    * 自定义异常
        >EXCEPTION
        WHEN NO_DATA_FOUND THEN...;//没有数据
        WHEN TOO_MANY_ROWS THEN...;//变量不能为多条记录赋值
        WHEN ZORE_DIVIDE THEN...;//除零错误
        WHEN OTHERS THEN...;//无指定异常处理时触发
    *  自定义异常抛出
    
        >IF A=A THNE RAISE e;
            WHEN e THEN ...;

* ###oracle伪列
    * rowid
    * rownum
    * currval和nextval
    >oracle中有sequence,用于生成序列对象，可设置增加步长，初始值，最大值，循环，cache
    * level
    * object_value

* ###游标
    ####1.属性获取
    * SQL%ISOPEN或者CUR%ISOPEN：布尔值，总是返回false，因为在游标连接结果集后就关闭；若是游标名，则返回游标打开的状态
    * SQL%ROWCOUNT或者CUR%ROWCOUNT：返回select结果集的记录数,FETCH结果集记录数
    * SQL%FOUND或者CUR%FOUND
    * SQL%NOTFOUND或者CUR%NOTFOUND
    >   游标名或者SQL都可以
    >   * NULL
    >   * TRUE:影响至少一条记录
    >   * FALSE:没有影响任何记录，也可用于检查delete是否生效  
    ####2.值获取
    * FETCH CUR INTO 字段，记录
    #### 3.传参
    > 形参可设置默认值，也可在打开的时候指定值
    > `DELCARE`
    > `CURSOR C (job VARCHAR2 DEFAULT 'Teacher', sal NUMBER) IS SELECT...`
    > `OPEN C (,1000)`
    > `OPEN C ('Engineer',1000)`
    ####4.游标不能在游标中，游标是指针

* ###REGEXP_LIKE()和LIKE
    > REGEXP_LIKE(var,pattern)是正则表达式函数(变量或者字段,模式）
    > LIKE 关键字，% _ 等字符串匹配,
    > 找一个表的列以 0 开始以 80 结束的长度为6位的数据,等价:
    >`SELECT * FROM staff  a  WHERE a.staff_code LIKE '0___80';`
`SELECT * FROM staff  a  WHERE  REGEXP_LIKE(a.staff_code,'0[0-9]{3}80');`
    
* ###order by， group by， distinct 冲突
    >  * select distinct 和order by一起使用的时候，order by中必须是常量或者select列表中出现的表达式
    >  * order by 的字段必须在group by中出现，或者是聚集函数
    >  * distinct和group 都能去重复，odistinct有排序过程，但是效率比group要高

##  Ｃ语言

*   ###系统函数sprintf(str1,'%s \n %s',str2,str3)
    > *  `str1 = str2 + '\n' + str3`,将str2，str3以'%s \n %s'的格式拼接放到str1中


*   二维数组技巧

    > *  取n行m列的元素可用 `array[n * m + m]`
    
*  指针
    > *  函数操作链表的头指针时，形参要用**，否则出了函数就头指针的修改就无效

*  库函数性能：尽量使用标准输入输出`scanf(),printf()`,效率、执行时间比`cin>>,cout<<`快很几倍以上
*  把string当作数组使用的时候：
    >  `#include<string>`
    >   `string a;`
    >  `getline(cin,a);`
    >  `a.size();a.[i];a.length;`
