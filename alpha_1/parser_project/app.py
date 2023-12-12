from flask import render_template, request, redirect
import parcer
import models

app = models.app
req = ''
cnt_get = None


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html'), 200


@app.route('/getbooks')
def getbooks():
    getbooks = models.db.session.query(models.Post).order_by(models.Post.id.desc()).limit(cnt_get).all()
    getbooks.reverse()
    title = req
    return render_template('getbooks.html', getbooks=getbooks, title=title), 200

@app.route('/myrequest', methods=['POST', 'GET'])
def myrequest():
    if request.method == 'POST':
        global req
        req = request.form['title']
        start_parser = parcer.parcer_start(req)
        data = start_parser[0]
        global cnt_get
        cnt_get = start_parser[1]
        for page in data:
            post = models.Post(title=page.get('title'),
                        author=page.get('author'),
                        price=page.get('price'),
                        publishing=page.get('publishing'),
                        year_release=page.get('year_release'),
                        pages=page.get('pages'),
                        description=page.get('description'),
                        url=page.get('url'))
            try:
                models.db.session.add(post)
                models.db.session.commit()
            except:
                return 'При добавлении данных в бд произошла ошибка'
        return redirect('/getbooks')
    else:
        return render_template('myrequest.html'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)