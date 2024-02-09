
# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from flask_cors import CORS
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship

# app = Flask(__name__)
# CORS(app)

# # Database Configuration
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pymssql://sa:1234@localhost/SugarianNavkar'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)

# ma = Marshmallow(app)

# class TenderHead(db.Model):
#     __tablename__ = 'nt_1_tender'
#     Tender_No = db.Column(db.Integer)
#     Company_Code = db.Column(db.Integer)
#     Tender_Date = db.Column(db.Date)
#     Lifting_Date = db.Column(db.Date)
#     Mill_Code = db.Column(db.Integer)
#     Grade = db.Column(db.String(50))
#     Quantal = db.Column(db.DECIMAL)
#     Packing =  db.Column(db.Integer)
#     Bags =  db.Column(db.Integer)
#     Payment_To =  db.Column(db.Integer)
#     Tender_From =  db.Column(db.Integer)
#     Tender_DO =  db.Column(db.Integer)
#     Voucher_By =  db.Column(db.Integer)
#     Broker =  db.Column(db.Integer)
#     Excise_Rate =  db.Column(db.DECIMAL)
#     Narration =  db.Column(db.String(500))
#     Mill_Rate =  db.Column(db.DECIMAL)
#     Created_By =  db.Column(db.String(50))
#     Modified_By =  db.Column(db.String(50))
#     Year_Code =  db.Column(db.Integer)
#     Purc_Rate =  db.Column(db.DECIMAL)
#     type =  db.Column(db.CHAR(1))
#     Branch_Id =  db.Column(db.Integer)
#     Voucher_No =  db.Column(db.Integer)
#     Sell_Note_No =  db.Column(db.String(50))
#     Brokrage =  db.Column(db.DECIMAL)
#     tenderid =  db.Column(db.Integer, primary_key=True)
#     mc =  db.Column(db.Integer)
#     itemcode =  db.Column(db.Integer)
#     season =  db.Column(db.String(20))
#     pt =  db.Column(db.Integer)
#     tf =  db.Column(db.Integer)
#     td =  db.Column(db.Integer)
#     vb =  db.Column(db.Integer)
#     bk =  db.Column(db.Integer)
#     ic =  db.Column(db.Integer)
#     gstratecode =  db.Column(db.Integer)
#     CashDiff =  db.Column(db.DECIMAL)
#     TCS_Rate =  db.Column(db.DECIMAL)
#     TCS_Amt =  db.Column(db.DECIMAL)
#     commissionid =  db.Column(db.Integer)

#     details = db.relationship('TenderDetails', backref='head', lazy=True)
 
# class TenderDetails(db.Model):
#     __tablename__ = 'nt_1_tenderdetails'

#     Tender_No = db.Column(db.Integer)
#     Company_Code = db.Column(db.Integer)
#     Buyer = db.Column(db.Integer)
#     Buyer_Quantal = db.Column(db.DECIMAL)
#     Sale_Rate = db.Column(db.DECIMAL)
#     Commission_Rate = db.Column(db.DECIMAL)
#     Sauda_Date = db.Column(db.Date)
#     Lifting_Date = db.Column(db.Date)
#     Narration = db.Column(db.String(255))
#     ID = db.Column(db.Integer)
#     Buyer_Party = db.Column(db.Integer)
#     AutoID = db.Column(db.Integer)
#     IsActive = db.Column(db.Integer)
#     year_code = db.Column(db.Integer)
#     Branch_Id = db.Column(db.Integer)
#     Delivery_Type = db.Column(db.String(10))
#     tenderid = db.Column(db.Integer, ForeignKey('nt_1_tender.tenderid'))
#     tenderdetailid = db.Column(db.Integer, primary_key=True)
#     buyerid = db.Column(db.Integer)
#     buyerpartyid = db.Column(db.Integer)
#     sub_broker = db.Column(db.Integer)
#     sbr = db.Column(db.Integer)
#     tcs_rate = db.Column(db.DECIMAL)
#     gst_rate = db.Column(db.DECIMAL)
#     tcs_amt = db.Column(db.DECIMAL)
#     gst_amt = db.Column(db.DECIMAL)
#     ShipTo = db.Column(db.Integer)
#     CashDiff = db.Column(db.DECIMAL)
#     shiptoid = db.Column(db.Integer)
    
#     tender = relationship('TenderHead', back_populates='details')
    

    
# class TenderHeadSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = TenderHead

# class TenderDetailsSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = TenderDetails
        
# tender_schema = TenderHeadSchema()
# # tender_schema = TenderHeadSchema(many=True)  

# tender_details_schema = TenderDetailsSchema()
# tender_details_schema = TenderDetailsSchema(many=True)  

# # Get All Users from Tender Head table
# @app.route("/users", methods=["GET"])
# def get_users():
#     all_users = TenderHead.query.all()
#     result = tender_schema.dump(all_users)
#     return jsonify(result)

     

# # Get data from both tables Tender Head and TenderDetail
# @app.route("/tender_data", methods=["GET"])
# def get_tender_data():
#     # Query both tables and get the data
#     tender_head_data = TenderHead.query.all()
#     tender_details_data = TenderDetails.query.all()

#     tender_head_result = tender_schema.dump(tender_head_data)
#     tender_details_result = tender_details_schema.dump(tender_details_data)

#     response = {
#         "tender_head_data": tender_head_result,
#         "tender_details_data": tender_details_result
#     }

#     return jsonify(response)


# # Insert TenderHead data in table
# @app.route("/insert_tender_head", methods=["POST"])
# def insert_tender_head():
#     try:
#         data = request.get_json()
#         headData = data['headData']


#         # Create TenderHead
#         new_head = TenderHead(**headData)
#         db.session.add(new_head)
#         db.session.commit()

#         # Serialize the inserted object using the schema
#         result = tender_schema.dump(new_head)

#         return jsonify({
#             "message": "TenderHead data inserted successfully",
#             "head": result
#         })

#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         return jsonify({"error": "Internal server error", "message": str(e)})


     

# from flask import jsonify

# @app.route("/insert_tender_head_detail", methods=["POST"])
# def insert_tender_head_detail():
#     try:
#         data = request.get_json()
#         headData = data['headData']
#         detailData = data['detailData']

#         try:
#             maxTenderNo = db.session.query(db.func.max(TenderHead.Tender_No)).scalar() or 0
#             newTenderNo = maxTenderNo + 1

#             # Update Tender_No in headData
#             headData['Tender_No'] = newTenderNo

#             # Create TenderHead
#             new_head = TenderHead(**headData)
#             db.session.add(new_head)

#             createdDetails = []
#             updatedDetails = []
#             deletedDetailIds = []

#             for item in detailData:
#                 if item['rowaction'] == "add":
#                     del item['rowaction'] 
#                     new_detail = TenderDetails(**item)
#                     new_head.details.append(new_detail) 
#                     createdDetails.append(new_detail)

#                 elif item['rowaction'] == "update":
#                     tenderdetailid = item['tenderdetailid']
#                     update_values = {k: v for k, v in item.items() if k not in ('tenderdetailid', 'tenderid')}
#                     del update_values['rowaction']  # Remove 'rowaction' field
#                     db.session.query(TenderDetails).filter(TenderDetails.tenderdetailid == tenderdetailid).update(update_values)
#                     updatedDetails.append(tenderdetailid)

#                 elif item['rowaction'] == "delete":
#                     tenderdetailid = item['tenderdetailid']
#                     detail_to_delete = db.session.query(TenderDetails).filter(TenderDetails.tenderdetailid == tenderdetailid).one_or_none()
    
#                     if detail_to_delete:
#                         db.session.delete(detail_to_delete)
#                         deletedDetailIds.append(tenderdetailid)

#             db.session.commit()

#             return jsonify({
#                 "message": "Data Inserted successfully",
#                 "head": tender_schema.dump(new_head),
#                 "addedDetails": tender_details_schema.dump(createdDetails),
#                 "updatedDetails": updatedDetails,
#                 "deletedDetailIds": deletedDetailIds
#             }), 201  # 201 Created

#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"error": "Internal server error", "message": str(e)}), 500  

#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Internal server error", "message": str(e)}), 500  

    
    

# @app.route("/update_sugar_purchase", methods=["PUT"])
# def update_sugar_purchase():
#     try:
#         # Retrieve 'tenderid' from URL parameters
#         tenderid = request.args.get('tenderid')

#         if tenderid is None:
#             return jsonify({"error": "Missing 'tenderid' parameter"}), 400  # 400 Bad Request

#         data = request.get_json()
#         headData = data['headData']
#         detailData = data['detailData']

#         try:
#             transaction = db.session.begin_nested()
            
#             # Update the head data
#             updatedHeadCount = db.session.query(TenderHead).filter(TenderHead.tenderid == tenderid).update(headData)
            
#             createdDetails = []
#             updatedDetails = []
#             deletedDetailIds = []

#             for item in detailData:
#                 if item['rowaction'] == "add":
#                     del item['rowaction'] 
#                     new_detail = TenderDetails(**item)
#                     db.session.add(new_detail)  # Add the new_detail to the session
#                     createdDetails.append(item)

#                 elif item['rowaction'] == "update":
#                     tenderdetailid = item['tenderdetailid']
#                     update_values = {k: v for k, v in item.items() if k not in ('tenderdetailid', 'tenderid')}
#                     del update_values['rowaction']  # Remove 'rowaction' field
#                     db.session.query(TenderDetails).filter(TenderDetails.tenderdetailid == tenderdetailid).update(update_values)
#                     updatedDetails.append(tenderdetailid)

#                 elif item['rowaction'] == "delete":
#                     tenderdetailid = item['tenderdetailid']
#                     detail_to_delete = db.session.query(TenderDetails).filter(TenderDetails.tenderdetailid == tenderdetailid).one_or_none()
    
#                     if detail_to_delete:
#                         db.session.delete(detail_to_delete)
#                         deletedDetailIds.append(tenderdetailid)

#             db.session.commit()

#             # Serialize the createdDetails
#             serialized_created_details = createdDetails 

#             return jsonify({
#                 "message": "Data Updated successfully",
#                 "updatedHeadCount": updatedHeadCount,
#                 "addedDetails": serialized_created_details,
#                 "updatedDetails": updatedDetails,
#                 "deletedDetailIds": deletedDetailIds
#             }), 200  # 200 OK

#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"error": "Internal server error", "message": str(e)}), 500 

#     except Exception as e:
#         return jsonify({"error": "Internal server error", "message": str(e)}), 500  
    
    
    
# @app.route("/delete_tender", methods=["DELETE"])
# def delete_tender():
#     try:
#         # Retrieve 'tenderid' from URL parameters
#         tenderid = request.args.get('tenderid')

#         if tenderid is None:
#             return jsonify({"error": "Missing 'tenderid' parameter"}), 400  # 400 Bad Request

#         tenderid = int(tenderid)  # Convert to integer if needed

#         # Check if the tender with the given tenderid exists in TenderHead
#         existing_tender_head = db.session.query(TenderHead).filter(TenderHead.tenderid == tenderid).first()

#         if existing_tender_head is None:
#             return jsonify({"error": "Tender not found"}), 404  # 404 Not Found

#         # Retrieve associated TenderDetails
#         associated_tender_details = existing_tender_head.details

#         # Delete the TenderHead record and associated TenderDetails records
#         db.session.delete(existing_tender_head)

#         for detail in associated_tender_details:
#             db.session.delete(detail)

#         db.session.commit()

#         return jsonify({"message": f"Tender with tenderid {tenderid} and associated details deleted successfully"}), 200 

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": "Internal server error", "message": str(e)}), 500 
    
    

# if __name__ == "__main__":
#     app.run(host='localhost', port=8080, debug=True)
    
    
    
    

# # # Get All Users
# # @app.route("/users", methods=["GET"])
# # def get_users():
# #     all_users = TenderHead.query.all()
# #     result = tender_schema.dump(all_users)
# #     return jsonify(result)

