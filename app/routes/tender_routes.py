# project_folder/app/routes/tender_routes.py
from flask import jsonify, request
from app import app, db
from app.models.tender import TenderHead, TenderDetails
from app.models.schemas import TenderHeadSchema, TenderDetailsSchema
from sqlalchemy.exc import SQLAlchemyError 
from sqlalchemy import text
from sqlalchemy import func
 
SQLALCHEMY_DATABASE_URI='mssql+pymssql://sa:1234@localhost/Sugarian'
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Define schemas
tender_schema = TenderHeadSchema()
# tender_schema = TenderHeadSchema(many=True)  


tender_details_schema = TenderDetailsSchema()
tender_details_schema = TenderDetailsSchema(many=True) 


# Get All Users from Tender Head table
@app.route("/users", methods=["GET"])
def get_users():
    all_users = TenderHead.query.all()
    result = tender_schema.dump(all_users)
    return jsonify(result)

@app.route("/get_last_tender_no", methods=["GET"])
def get_last_tender_no():
    try:
        # Use SQLAlchemy to get the maximum Tender_No from the TenderHead table
        last_tender_no = db.session.query(func.max(TenderHead.Tender_No)).scalar()

        return jsonify({"lastTenderNo": last_tender_no}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500    
    
    

# Get data from both tables Tender Head and TenderDetail
@app.route("/tender_data_all", methods=["GET"])
def get_tender_data():
    try:
        # Query both tables and get the data
        tender_head_data = TenderHead.query.all()
        tender_details_data = TenderDetails.query.all()

        tender_head_result = tender_schema.dump(tender_head_data)
        tender_details_result = tender_details_schema.dump(tender_details_data)

        response = {
            "tender_head_data": tender_head_result,
            "tender_details_data": tender_details_result
        }

        return jsonify(response), 200

    except Exception as e:
        # Handle any potential exceptions and return an error response with a 500 Internal Server Error status code
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
    
@app.route("/get_last_tender_data", methods=["GET"])
def get_last_tender_data():
    try:
        # Use SQLAlchemy to get the last record from the TenderHead table
        last_tender_head = TenderHead.query.order_by(TenderHead.tenderid.desc()).first()

        if last_tender_head is None:
            return jsonify({"error": "No records found in TenderHead table"}), 404

        # Get the last tenderid
        last_tenderid = last_tender_head.tenderid

        # Query the TenderDetails table for the last record with the corresponding tenderid
        last_tender_details = TenderDetails.query.filter_by(tenderid=last_tenderid).all()

        # Serialize the data using the schemas
        tender_head_result = tender_schema.dump(last_tender_head)
        tender_details_result = tender_details_schema.dump(last_tender_details)

        response = {
            "last_tender_head_data": tender_head_result,
            "last_tender_details_data": tender_details_result
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



# Insert TenderHead data in table
@app.route("/insert_tender_head", methods=["POST"])
def insert_tender_head():
    try:
        data = request.get_json()
        headData = data['headData']


        # Create TenderHead
        new_head = TenderHead(**headData)
        db.session.add(new_head)
        db.session.commit()

        # Serialize the inserted object using the schema
        result = tender_schema.dump(new_head)

        return jsonify({
            "message": "TenderHead data inserted successfully",
            "head": result
        })

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": str(e)})


     

@app.route("/insert_tender_head_detail", methods=["POST"])
def insert_tender_head_detail():
    try:
        data = request.get_json()
        headData = data['headData']
        detailData = data['detailData']

        try:
            maxTenderNo = db.session.query(db.func.max(TenderHead.Tender_No)).scalar() or 0
            print(maxTenderNo)
            newTenderNo = maxTenderNo + 1

            # Update Tender_No in headData
            headData['Tender_No'] = newTenderNo

            # Create TenderHead
            new_head = TenderHead(**headData)
            db.session.add(new_head)

            createdDetails = []
            updatedDetails = []
            deletedDetailIds = []

            for item in detailData:
                
                item['Tender_No'] = newTenderNo
                
                if item['rowaction'] == "add":
                    del item['rowaction'] 
                    new_detail = TenderDetails(**item)
                    new_head.details.append(new_detail) 
                    createdDetails.append(new_detail)

                elif item['rowaction'] == "update":
                    tenderdetailid = item['tenderdetailid']
                    update_values = {k: v for k, v in item.items() if k not in ('tenderdetailid', 'tenderid')}
                    del update_values['rowaction']  # Remove 'rowaction' field
                    db.session.query(TenderDetails).filter(TenderDetails.tenderdetailid == tenderdetailid).update(update_values)
                    updatedDetails.append(tenderdetailid)


                elif item['rowaction'] == "delete":
                    tenderdetailid = item['tenderdetailid']
                    detail_to_delete = db.session.query(TenderDetails).filter(TenderDetails.tenderdetailid == tenderdetailid).one_or_none()
    
                    if detail_to_delete:
                        db.session.delete(detail_to_delete)
                        deletedDetailIds.append(tenderdetailid)

            db.session.commit()

            return jsonify({
                "message": "Data Inserted successfully",
                "head": tender_schema.dump(new_head),
                "addedDetails": tender_details_schema.dump(createdDetails),
                "updatedDetails": updatedDetails,
                "deletedDetailIds": deletedDetailIds
            }), 201  # 201 Created

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"error": "Internal server error", "message": str(e)}), 500  

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error", "message": str(e)}), 500  

    
@app.route("/update_sugar_purchase", methods=["PUT"])
def update_sugar_purchase():
    try:
        # Retrieve 'tenderid' from URL parameters
        tenderid = request.args.get('tenderid')

        if tenderid is None:
            return jsonify({"error": "Missing 'tenderid' parameter"}), 400  
        data = request.get_json()
        headData = data['headData']
        detailData = data['detailData']

        try:
            transaction = db.session.begin_nested()
            
            # Update the head data
            updatedHeadCount = db.session.query(TenderHead).filter(TenderHead.tenderid == tenderid).update(headData)
            

            createdDetails = []
            updatedDetails = []
            deletedDetailIds = []

            updated_tender_head = db.session.query(TenderHead).filter(TenderHead.tenderid == tenderid).one()
            tender_no = updated_tender_head.Tender_No


            for item in detailData:
                if item['rowaction'] == "add":
                    item['Tender_No'] = tender_no
                    item['tenderid'] = tenderid
                    del item['rowaction'] 
                    new_detail = TenderDetails(**item)
                    db.session.add(new_detail) 
                    createdDetails.append(item)

                elif item['rowaction'] == "update":
                    item['Tender_No'] = tender_no
                    item['tenderid'] = tenderid
                    tenderdetailid = item['tenderdetailid']
                    update_values = {k: v for k, v in item.items() if k not in ('tenderdetailid', 'tenderid')}
                    del update_values['rowaction'] 
                    db.session.query(TenderDetails).filter(TenderDetails.tenderdetailid == tenderdetailid).update(update_values)
                    updatedDetails.append(tenderdetailid)

                elif item['rowaction'] == "delete":
                    tenderdetailid = item['tenderdetailid']
                    detail_to_delete = db.session.query(TenderDetails).filter(TenderDetails.tenderdetailid == tenderdetailid).one_or_none()
    
                    if detail_to_delete:
                        db.session.delete(detail_to_delete)
                        deletedDetailIds.append(tenderdetailid)

            db.session.commit()

            # Serialize the createdDetails
            serialized_created_details = createdDetails 

            return jsonify({
                "message": "Data Updated successfully",
                "updatedHeadCount": updatedHeadCount,
                "addedDetails": serialized_created_details,
                "updatedDetails": updatedDetails,
                "deletedDetailIds": deletedDetailIds
            }), 200 

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Internal server error", "message": str(e)}), 500 

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500  
    
    
    
@app.route("/delete_tender", methods=["DELETE"])
def delete_tender():
    try:
        # Retrieve 'tenderid' from URL parameters
        tenderid = request.args.get('tenderid')

        if tenderid is None:
            return jsonify({"error": "Missing 'tenderid' parameter"}), 400  

        tenderid = int(tenderid)  

        # Check if the tender with the given tenderid exists in TenderHead
        existing_tender_head = db.session.query(TenderHead).filter(TenderHead.tenderid == tenderid).first()

        if existing_tender_head is None:
            return jsonify({"error": "Tender not found"}), 404  

        # Retrieve associated TenderDetails
        associated_tender_details = existing_tender_head.details

        # Delete the TenderHead record and associated TenderDetails records
        db.session.delete(existing_tender_head)

        for detail in associated_tender_details:
            db.session.delete(detail)

        db.session.commit()

        return jsonify({"message": f"Tender with tenderid {tenderid} and associated details deleted successfully"}), 200 

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": str(e)}), 500 
    
    

@app.route('/getData_query', methods=['GET'])
def get_data():

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
    
    
# New route to get the first record from the database
@app.route("/get_first_tender_data", methods=["GET"])
def get_first_tender_data():
    try:
        # Use SQLAlchemy to get the first record from the TenderHead table
        first_tender_head = TenderHead.query.order_by(TenderHead.tenderid).first()

        if first_tender_head is None:
            return jsonify({"error": "No records found in TenderHead table"}), 404

        # Get the tenderid of the first record
        first_tenderid = first_tender_head.tenderid

        # Query the TenderDetails table for the first record with the corresponding tenderid
        first_tender_details = TenderDetails.query.filter_by(tenderid=first_tenderid).all()

        # Serialize the data using the schemas
        first_tender_head_result = tender_schema.dump(first_tender_head)
        first_tender_details_result = tender_details_schema.dump(first_tender_details)

        response = {
            "first_tender_head_data": first_tender_head_result,
            "first_tender_details_data": first_tender_details_result
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
    
# New route to get the last record from the database
@app.route("/get_last_tender_data_Navigation", methods=["GET"])
def get_last_tender_data_Navigation():
    try:
        # Use SQLAlchemy to get the last record from the TenderHead table
        last_tender_head = TenderHead.query.order_by(TenderHead.tenderid.desc()).first()

        if last_tender_head is None:
            return jsonify({"error": "No records found in TenderHead table"}), 404

        # Get the tenderid of the last record
        last_tenderid = last_tender_head.tenderid

        # Query the TenderDetails table for the last record with the corresponding tenderid
        last_tender_details = TenderDetails.query.filter_by(tenderid=last_tenderid).all()

        # Serialize the data using the schemas
        last_tender_head_result = tender_schema.dump(last_tender_head)
        last_tender_details_result = tender_details_schema.dump(last_tender_details)

        response = {
            "last_tender_head_data": last_tender_head_result,
            "last_tender_details_data": last_tender_details_result
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# New route to get the previous record from the database
@app.route("/get_previous_tender_data", methods=["GET"])
def get_previous_tender_data():
    try:
        current_tender_no = request.args.get("current_tender_no")

        # Check if the current_tender_no is provided
        if current_tender_no is None:
            return jsonify({"error": "Current tender number is required"}), 400

        # Use SQLAlchemy to get the previous record from the TenderHead table
        previous_tender_head = TenderHead.query.filter(TenderHead.Tender_No < current_tender_no).order_by(
            TenderHead.Tender_No.desc()).first()

        if previous_tender_head is None:
            return jsonify({"error": "No previous records found"}), 404

        # Get the tender number of the previous record
        previous_tender_no = previous_tender_head.Tender_No

        # Query the TenderDetails table for the previous record with the corresponding tender number
        previous_tender_details = TenderDetails.query.filter_by(Tender_No=previous_tender_no).all()

        # Serialize the data using the schemas
        previous_tender_head_result = tender_schema.dump(previous_tender_head)
        previous_tender_details_result = tender_details_schema.dump(previous_tender_details)

        response = {
            "previous_tender_head_data": previous_tender_head_result,
            "previous_tender_details_data": previous_tender_details_result
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
    
    
    
# New route to get the next record from the database
@app.route("/get_next_tender_data", methods=["GET"])
def get_next_tender_data():
    try:
        current_tender_no = request.args.get("current_tender_no")

        # Check if the current_tender_no is provided
        if current_tender_no is None:
            return jsonify({"error": "Current tender number is required"}), 400

        # Use SQLAlchemy to get the next record from the TenderHead table
        next_tender_head = TenderHead.query.filter(TenderHead.Tender_No > current_tender_no).order_by(
            TenderHead.Tender_No.asc()).first()

        if next_tender_head is None:
            return jsonify({"error": "No next records found"}), 404

        # Get the tender number of the next record
        next_tender_no = next_tender_head.Tender_No

        # Query the TenderDetails table for the next record with the corresponding tender number
        next_tender_details = TenderDetails.query.filter_by(Tender_No=next_tender_no).all()

        # Serialize the data using the schemas
        next_tender_head_result = tender_schema.dump(next_tender_head)
        next_tender_details_result = tender_details_schema.dump(next_tender_details)

        response = {
            "next_tender_head_data": next_tender_head_result,
            "next_tender_details_data": next_tender_details_result
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# Utility Get Call
@app.route("/all_tender_data", methods=["GET"])
def get_all_tender_data():
    try:
        sql_query = """
            SELECT ROW_NUMBER() OVER (ORDER BY Tender_No DESC) AS RowNumber,
                   Tender_No,
                   Tender_DateConverted AS Tender_Date,
                   millshortname,
                   Quantal,
                   Grade,
                   Mill_Rate,
                   paymenttoname,
                   tenderdoname,
                   season,
                   brokershortname,
                   Lifting_DateConverted AS Lifting_Date,
                   tenderid,
                   Mill_Code
            FROM qrytenderhead
            WHERE Company_Code = 4
            ORDER BY Tender_No DESC
        """

        # Execute the SQL query
        result = db.session.execute(text(sql_query))

        # Fetch all rows and convert each row to a dictionary
        response = []
        for row in result:
            response.append({
                'Tender_No': row.Tender_No,
                'Tender_Date': row.Tender_Date,
                'millshortname': row.millshortname,
                'Quantal': row.Quantal,
                'Grade': row.Grade,
                'Mill_Rate': row.Mill_Rate,
                'paymenttoname': row.paymenttoname,
                'tenderdoname': row.tenderdoname,
                'Lifting_Date': row.Lifting_Date,
                'tenderid': row.tenderid,
                'Mill_Code': row.Mill_Code,
            })

        return jsonify(response),200
        

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500








