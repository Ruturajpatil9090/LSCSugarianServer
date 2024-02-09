from flask import jsonify
from app import app, db  
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

@app.route('/gst_rate_master', methods=['GET'])
def gst_rate_master():
    try:
        # Start a database transaction
        with db.session.begin_nested():
            query = db.session.execute(text('''
                SELECT Doc_no, GST_Name, Rate
                FROM NT_1_GSTRateMaster
                WHERE Company_Code=1
            '''))

            result = query.fetchall()

        response = []
        for row in result:
            response.append({
                'Doc_no': row.Doc_no,
                'GST_Name': row.GST_Name,
                'Rate': row.Rate
            })

        return jsonify(response)

    except SQLAlchemyError as error:
        print("Error fetching data:", error)
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
