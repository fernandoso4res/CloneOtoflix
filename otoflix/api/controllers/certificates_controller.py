from io import BytesIO
import sys
import htmlmin
import img2pdf
import imgkit
from flask import render_template, request, jsonify, send_file
from controllers.errors_controller import errors
from repositories.mongodb_repository import find_one, normalize_id
from ext.auth import get_jwt_identity
from config import CERTIFICATE_BACKGROUND_IMAGE_URL, CERTIFICATE_FONT_PERSON_NAME_URL, CERTIFICATE_FONT_COURSE_NAME_URL, CERTIFICATE_FONT_COURSE_HOURS_URL, CERTIFICATE_FONT_COMPLETION_DATE_URL


def get_certificates():
    try:
        if not request.args.get('course_id'):
            return jsonify(msg="Course id not informed"), 400
        course_id = normalize_id(request.args.get('course_id'))
        id = get_jwt_identity()
        elemMatch = {'$elemMatch': {'courses_completed': { '$elemMatch': { 'id_course': course_id } }}}
        user = find_one('users', elemMatch,'first_name', 'last_name', id = id )
        if 'courses_completed' in user:
            dados = {'first_name': user['first_name'],
                'last_name': user['last_name'],
                'course_name': user['courses_completed'][0]['course_name'].upper(),
                'course_hours': user['courses_completed'][0]['course_hours'].upper(),
                'completion_date': user['courses_completed'][0]['completion_date'].strftime("%d/%m/%Y"),
                'certificate_background_image_url': CERTIFICATE_BACKGROUND_IMAGE_URL,
                'certificate_font_person_name_url': CERTIFICATE_FONT_PERSON_NAME_URL,
                'certificate_font_course_name_url': CERTIFICATE_FONT_COURSE_NAME_URL,
                'certificate_font_course_hours_url': CERTIFICATE_FONT_COURSE_HOURS_URL,
                'certificate_font_completion_date_url': CERTIFICATE_FONT_COMPLETION_DATE_URL,
            }
            html = render_template('certificado/certificado.html', **dados)
            html = htmlmin.minify(html,remove_empty_space=True)
            img = imgkit.from_string(html, False)
            pdf = img2pdf.convert(img)
            return send_file(BytesIO(pdf), mimetype='application/pdf'), 200
        else:
            return jsonify(msg="Invalid course id"), 400
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error generating certificate"), 500