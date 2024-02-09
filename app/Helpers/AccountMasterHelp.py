
from flask import jsonify
from app import app, db
from sqlalchemy.exc import SQLAlchemyError 
from sqlalchemy import text


@app.route('/account_master_all', methods=['GET'])
def account_master_all():

    try:
        # Start a database transaction
        with db.session.begin_nested():
            query = db.session.execute(text('''
                SELECT dbo.nt_1_accountmaster.Ac_Code, dbo.nt_1_accountmaster.Ac_Name_E, dbo.nt_1_citymaster.city_name_e as cityname, dbo.nt_1_accountmaster.Gst_No, dbo.nt_1_accountmaster.accoid 
                FROM dbo.nt_1_accountmaster 
                LEFT OUTER JOIN dbo.nt_1_citymaster ON dbo.nt_1_accountmaster.City_Code = dbo.nt_1_citymaster.city_code AND dbo.nt_1_accountmaster.company_code = dbo.nt_1_citymaster.company_code 
                WHERE Locked=0 AND dbo.nt_1_accountmaster.Ac_type='M' AND dbo.nt_1_accountmaster.Company_Code=1
                ORDER BY Ac_Name_E DESC
            '''))

            result = query.fetchall()

        response = []
        for row in result:
            response.append({
                'Ac_Code': row.Ac_Code,
                'Ac_Name_E': row.Ac_Name_E,
                'cityname': row.cityname,
                'Gst_No': row.Gst_No,
                'accoid': row.accoid
            })

        return jsonify(response)

    except SQLAlchemyError as error:
        # Handle database errors
        print("Error fetching data:", error)
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
