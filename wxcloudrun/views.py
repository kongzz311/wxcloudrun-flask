from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wxcloudrun.mapper import *

locations = ['崇明区-城桥镇',
 '崇明区-堡镇',
 '崇明区-向化镇',
 '崇明区-港沿镇',
 '崇明区-中兴镇',
 '崇明区-绿华镇',
 '崇明区-港西镇',
 '崇明区-新海镇',
 '崇明区-新村乡',
 '崇明区-横沙乡',
 '崇明区-东平林场',
 '崇明区-庙镇',
 '崇明区-建设镇',
 '崇明区-新河镇',
 '崇明区-竖新镇',
 '崇明区-陈家镇',
 '崇明区-东平镇',
 '崇明区-长兴镇',
 '崇明区-上实现代农业园区',
 '崇明区-三星镇',
 '浦东新区-潍坊新村街道',
 '浦东新区-陆家嘴街道',
 '浦东新区-周家渡街道',
 '浦东新区-塘桥街道',
 '浦东新区-上钢新村街道',
 '浦东新区-南码头路街道',
 '浦东新区-沪东新村街道',
 '浦东新区-金杨新村街道',
 '浦东新区-洋泾街道',
 '浦东新区-浦兴路街道',
 '浦东新区-东明路街道',
 '浦东新区-花木街道',
 '浦东新区-川沙新镇',
 '浦东新区-高桥镇',
 '浦东新区-北蔡镇',
 '浦东新区-合庆镇',
 '浦东新区-唐镇',
 '浦东新区-曹路镇',
 '浦东新区-金桥镇',
 '浦东新区-高行镇',
 '浦东新区-高东镇',
 '浦东新区-张江镇',
 '浦东新区-惠南镇',
 '浦东新区-周浦镇',
 '浦东新区-新场镇',
 '浦东新区-大团镇',
 '浦东新区-康桥镇',
 '浦东新区-泥城镇',
 '浦东新区-宣桥镇',
 '浦东新区-书院镇',
 '浦东新区-万祥镇',
 '浦东新区-老港镇',
 '浦东新区-南汇新城镇',
 '浦东新区-三林镇',
 '浦东新区-祝桥镇',
 '浦东新区-航头镇',
 '奉贤区-奉浦社区',
 '奉贤区-海湾镇',
 '奉贤区-金汇镇',
 '奉贤区-奉城镇',
 '奉贤区-奉浦街道',
 '奉贤区-金海街道',
 '奉贤区-西渡街道',
 '奉贤区-四团镇',
 '奉贤区-南桥镇',
 '奉贤区-庄行镇',
 '奉贤区-青村镇',
 '奉贤区-柘林镇',
 '金山区-石化街道',
 '金山区-朱泾镇',
 '金山区-金山卫镇',
 '金山区-亭林镇',
 '金山区-吕巷镇',
 '金山区-枫泾镇',
 '金山区-张堰镇',
 '金山区-廊下镇',
 '金山区-漕泾镇',
 '金山区-山阳镇',
 '普陀区-曹杨新村街道',
 '普陀区-长风新村街道',
 '普陀区-长寿路街道',
 '普陀区-石泉路街道',
 '普陀区-长征镇',
 '普陀区-真如镇街道',
 '普陀区-甘泉路街道',
 '普陀区-宜川路街道',
 '普陀区-万里街道',
 '普陀区-桃浦镇',
 '黄浦区-豫园街道',
 '黄浦区-老西门街道',
 '黄浦区-打浦桥街道',
 '黄浦区-小东门街道',
 '黄浦区-淮海中路街道',
 '黄浦区-外滩街道',
 '黄浦区-半淞园路街道',
 '黄浦区-瑞金二路街道',
 '黄浦区-南京东路街道',
 '黄浦区-五里桥街道',
 '杨浦区-定海路街道',
 '杨浦区-平凉路街道',
 '杨浦区-江浦路街道',
 '杨浦区-四平路街道',
 '杨浦区-控江路街道',
 '杨浦区-长白新村街道',
 '杨浦区-延吉新村街道',
 '杨浦区-殷行街道',
 '杨浦区-大桥街道',
 '杨浦区-五角场街道',
 '杨浦区-新江湾城街道',
 '杨浦区-长海路街道',
 '虹口区-嘉兴路街道',
 '虹口区-广中路街道',
 '虹口区-凉城新村街道',
 '虹口区-江湾镇街道',
 '虹口区-欧阳路街道',
 '虹口区-曲阳路街道',
 '虹口区-四川北路街道',
 '虹口区-北外滩街道',
 '徐汇区-湖南路街道',
 '徐汇区-枫林路街道',
 '徐汇区-天平路街道',
 '徐汇区-斜土路街道',
 '徐汇区-华泾镇',
 '徐汇区-凌云路街道',
 '徐汇区-长桥街道',
 '徐汇区-龙华街道',
 '徐汇区-康健新村街道',
 '徐汇区-徐家汇街道',
 '徐汇区-田林街道',
 '徐汇区-漕河泾街道',
 '徐汇区-虹梅路街道',
 '青浦区-夏阳街道',
 '青浦区-徐泾镇',
 '青浦区-盈浦街道',
 '青浦区-香花桥街道',
 '青浦区-金泽镇',
 '青浦区-练塘镇',
 '青浦区-朱家角镇',
 '青浦区-重固镇',
 '青浦区-白鹤镇',
 '青浦区-赵巷镇',
 '青浦区-华新镇',
 '长宁区-江苏路街道',
 '长宁区-周家桥街道',
 '长宁区-仙霞新村街道',
 '长宁区-新泾镇',
 '长宁区-新华路街道',
 '长宁区-北新泾街道',
 '长宁区-程家桥街道',
 '长宁区-虹桥街道',
 '长宁区-天山路街道',
 '长宁区-华阳路街道',
 '静安区-石门二路街道',
 '静安区-北站街道',
 '静安区-江宁路街道',
 '静安区-天目西路街道',
 '静安区-共和新路街道',
 '静安区-宝山路街道',
 '静安区-静安寺街道',
 '静安区-曹家渡街道',
 '静安区-南京西路街道',
 '静安区-大宁路街道',
 '静安区-芷江西路街道',
 '静安区-临汾路街道',
 '静安区-彭浦新村街道',
 '静安区-彭浦镇',
 '宝山区-友谊路街道',
 '宝山区-吴淞街道',
 '宝山区-张庙街道',
 '宝山区-罗店镇',
 '宝山区-大场镇',
 '宝山区-杨行镇',
 '宝山区-月浦镇',
 '宝山区-罗泾镇',
 '宝山区-顾村镇',
 '宝山区-高境镇',
 '宝山区-庙行镇',
 '宝山区-淞南镇',
 '松江区-岳阳街道',
 '松江区-永丰街道',
 '松江区-新桥镇',
 '松江区-叶榭镇',
 '松江区-广富林街道',
 '松江区-方松街道',
 '松江区-中山街道',
 '松江区-石湖荡镇',
 '松江区-泗泾镇',
 '松江区-泖港镇',
 '松江区-九里亭街道',
 '松江区-九亭镇',
 '松江区-小昆山镇',
 '松江区-洞泾镇',
 '松江区-新浜镇',
 '松江区-佘山镇',
 '松江区-车墩镇',
 '嘉定区-新成路街道',
 '嘉定区-真新街道',
 '嘉定区-菊园新区',
 '嘉定区-南翔镇',
 '嘉定区-嘉定镇街道',
 '嘉定区-江桥镇',
 '嘉定区-徐行镇',
 '嘉定区-马陆镇',
 '嘉定区-华亭镇',
 '嘉定区-外冈镇',
 '嘉定区-安亭镇',
 '闵行区-江川路街道',
 '闵行区-新虹街道',
 '闵行区-浦锦街道',
 '闵行区-古美街道',
 '闵行区-莘庄镇',
 '闵行区-七宝镇',
 '闵行区-虹桥镇',
 '闵行区-颛桥镇',
 '闵行区-华漕镇',
 '闵行区-吴泾镇',
 '闵行区-梅陇镇',
 '闵行区-马桥镇',
 '闵行区-浦江镇']

@app.route("/")
def index():
    return render_template('index.html', locations=locations)


@app.route('/addUser', methods=['POST','GET'])
def addUserController():
    if request.method == 'GET':
        return render_template('index.html', locations=locations)
    else:
        result = request.form
        location = result['location']
        id = result['id']
        qu = location.split('-')[0]
        jie = location.split('-')[1]
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
            print(request.environ['REMOTE_ADDR'])
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
            print(request.environ['HTTP_X_FORWARDED_FOR'])

        print(ip)
        addUser(qu, jie, id, ip)
        return render_template('index.html', locations=locations, msg='添加成功')


@app.route('/getUser', methods=['POST','GET'])
def getUserController():
    if request.method == 'GET':
        return render_template('index.html', locations=locations)
    else:
        result = request.form
        id = result['id']
        data = getUser(id)
        msg = ''
        ip = request.environ['REMOTE_ADDR']
        print(ip)
        if data is None or data.get('del', True) is True:
            msg = '没有查询到'
        else:
            msg = '位置是：'+data['qu']+'-'+data['jie']
        return render_template('index.html', locations=locations, msg=msg)

@app.route('/delUser', methods=['POST','GET'])
def delUserController():
    if request.method == 'GET':
        return render_template('index.html', locations=locations)
    else:
        result = request.form
        id = result['id']
        data = delUser(id)
        print(data)
        msg = ''
        if data is None or data.get('del', True) is True:
            msg = '数据库中无此id'
        else:
            msg = '删除成功'
        return render_template('index.html', locations=locations, msg=msg)

@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
