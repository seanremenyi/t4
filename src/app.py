from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET, S3_URL
from filters import datetimeformat, file_type
from botocore.client import Config
import json

s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
    )


app = Flask(__name__)
Bootstrap(app)
app.secret_key= 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type


# @app.route('/')
# def index():
#     return render_template('index.html')
    
@app.route('/')
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()
    
    return render_template('files.html', my_bucket=my_bucket, files=summaries)
    



@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    s3_resource= boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(file.filename).put(Body=file)


    
    flash('File uploaded successfully')
    return redirect(url_for('files'))
    
@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    s3_resource= boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(key).delete()
    
    flash('File deleted successfully')
    return redirect(url_for('files'))
    
@app.route('/scan', methods=['POST'])
def scan():
    key = str(request.form['key'])

    s3_resource= boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    client = boto3.client('rekognition')
    pic=str(S3_URL) + str(key)
    response = client.detect_faces(
    Image={
        'S3Object': {
            'Bucket': S3_BUCKET,
            'Name': key
        }
    },
    Attributes=[
        'ALL'
    ]
)
    base= response["FaceDetails"][0]
    ageH = json.dumps(base["AgeRange"]["High"])
    ageL = json.dumps(base["AgeRange"]["Low"])
    beard= json.dumps(base["Beard"]["Value"])
    beardconf= json.dumps(base["Beard"]["Confidence"])


    happy=json.dumps(base["Emotions"][0]["Type"])
    happyconf=json.dumps(base["Emotions"][0]["Confidence"])
    calm=json.dumps(base["Emotions"][1]["Type"])
    calmconf=json.dumps(base["Emotions"][1]["Confidence"])
    surprised=json.dumps(base["Emotions"][2]["Type"])
    surprisedconf=json.dumps(base["Emotions"][2]["Confidence"])
    disgusted=json.dumps(base["Emotions"][3]["Type"])
    disgustedconf=json.dumps(base["Emotions"][3]["Confidence"])
    confused=json.dumps(base["Emotions"][4]["Type"])
    confusedconf=json.dumps(base["Emotions"][4]["Confidence"])
    fear=json.dumps(base["Emotions"][5]["Type"])
    fearconf=json.dumps(base["Emotions"][5]["Confidence"])
    angry=json.dumps(base["Emotions"][6]["Type"])
    angryconf=json.dumps(base["Emotions"][6]["Confidence"])
    sad=json.dumps(base["Emotions"][7]["Type"])
    sadconf=json.dumps(base["Emotions"][7]["Confidence"])
    
    glasses= json.dumps(base["Eyeglasses"]["Value"])
    glassesconf= json.dumps(base["Eyeglasses"]["Confidence"])
    eyes= json.dumps(base["EyesOpen"]["Value"])
    eyesconf= json.dumps(base["EyesOpen"]["Confidence"])
    gender= json.dumps(base["Gender"]["Value"])
    genderconf= json.dumps(base["Gender"]["Confidence"])
    mustache= json.dumps(base["Mustache"]["Value"])
    mustacheconf= json.dumps(base["Mustache"]["Confidence"])
    
    smile= json.dumps(base["Smile"]["Value"])
    smileconf= json.dumps(base["Smile"]["Confidence"])
    sunglasses= json.dumps(base["Sunglasses"]["Value"])
    sunglassesconf= json.dumps(base["Sunglasses"]["Confidence"])
    mouth= json.dumps(base["MouthOpen"]["Value"])
    mouthconf= json.dumps(base["MouthOpen"]["Confidence"])

 
    return render_template('results.html', pic=pic, mouthconf=mouthconf, happy=happy, happyconf=happyconf, calm=calm, calmconf=calmconf, surprised=surprised, surprisedconf=surprisedconf, disgusted=disgusted,sad=sad, sadconf=sadconf, beard=beard, beardconf=beardconf, ageL=ageL, ageH=ageH,disgustedconf=disgustedconf, confused=confused, confusedconf=confusedconf, fear=fear, fearconf=fearconf, angry=angry, angryconf=angryconf, smile=smile, smileconf=smileconf, mustache=mustache, mustacheconf=mustacheconf, gender=gender, genderconf=genderconf, eyes=eyes, eyesconf=eyesconf, glasses=glasses, glassesconf=glassesconf, mouth=mouth, sunglasses=sunglasses, sunglassesconf=sunglassesconf)
    
if __name__ == '__main__':
    app.run()