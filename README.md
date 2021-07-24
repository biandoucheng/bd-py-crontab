# 基于python3.5 开发的仿照linux的crontab的任务调度器
## 使用注意事项
### crontab 是核心文件夹勿动
### camp及tasks文件夹是示例可仿照使用
### camp是任务执行的入口文件夹
### camp里面包含了run_schedule包，这里是用户自定义任务执行中的钩子方法的地方
### camp里的run_task包是填写配置信息的地方，包含项目根目录，配置文件目录，任务实例目录等
### 每个任务实例都需要一个供调度器执行的run()方法，在该方法中完成对任务方法的调用
### Please enjoy it .
