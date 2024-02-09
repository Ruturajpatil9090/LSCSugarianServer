from flask import jsonify
from app import app, db 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

@app.route('/system_master', methods=['GET'])
def system_master():
    try:
        # Start a database transaction
        with db.session.begin_nested():
            query = db.session.execute(text('''
                SELECT System_Code, System_Name_E AS Item_Name, KgPerKatta,system_type
                FROM nt_1_systemmaster
                WHERE Company_Code=1
            '''))

            result = query.fetchall()

        response = []
        for row in result:
            response.append({
                'System_Code': row.System_Code,
                'Item_Name': row.Item_Name,
                'KgPerKatta': row.KgPerKatta,
                'system_type': row.system_type
            })

        return jsonify(response)

    except SQLAlchemyError as error:
        # Handle database errors
        print("Error fetching data:", error)
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


