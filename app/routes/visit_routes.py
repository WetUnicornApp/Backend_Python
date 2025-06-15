from datetime import datetime
from http.client import responses

from flask import Blueprint, request

from app.models.calendar_models.calendar import Calendar
from app.models.visit_models.visit import Visit
from app.models.visit_models.visit_animal import VisitAnimal
from app.models.visit_models.visit_employee import VisitEmployee
from app.repositories.animal_repository import AnimalRepository
from app.repositories.calendar_repository import CalenderRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.visits_repository.visit_animal_repository import VisitAnimalRepository
from app.repositories.visits_repository.visit_repository import VisitRepository
from app.repositories.visits_repository.visits_employee_repository import VisitEmployeeRepository
from app.schemas.Visit_chema.calender_schema import CalenderSchema
from app.schemas.Visit_chema.visit_employee_schema import VisitEmployeeSchema
from app.schemas.Visit_chema.visit_schema import VisitSchema
from app.services.service import Service
from app.utils.api_response import ApiResponse
from config.database import SessionLocal

# from Backend_Python.app.utils.api_response import ApiResponse

visit_bp = Blueprint('visit', __name__)



from datetime import datetime
from http.client import responses

from flask import Blueprint, request

from app.models.calendar_models.calendar import Calendar
from app.models.visit_models.visit import Visit
from app.models.visit_models.visit_employee import VisitEmployee
from app.repositories.animal_repository import AnimalRepository
from app.repositories.calendar_repository import CalenderRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.visits_repository.visit_repository import VisitRepository
from app.repositories.visits_repository.visits_employee_repository import VisitEmployeeRepository
from app.schemas.Visit_chema.calender_schema import CalenderSchema
from app.schemas.Visit_chema.visit_employee_schema import VisitEmployeeSchema
from app.schemas.Visit_chema.visit_schema import VisitSchema
from app.services.service import Service
from app.utils.api_response import ApiResponse
from config.database import SessionLocal

# from Backend_Python.app.utils.api_response import ApiResponse

visit_bp = Blueprint('visit', __name__)



@visit_bp.route('/create', methods=['POST'])
def create_visit():
    session = SessionLocal()

    try:
        data = request.get_json()
        datetime_planned = data.get("datetime_planned", datetime.utcnow())
        employee_id = data.get("employee_id")

        if employee_id:
            existing_visit_ids = session.query(VisitEmployee.visit_id).filter_by(employee_id=employee_id).all()
            visit_ids = [v[0] for v in existing_visit_ids]

            if visit_ids:
                conflicting = session.query(Visit).join(Calendar).filter(
                    Visit.id.in_(visit_ids),
                    Calendar.datetime_planned == datetime_planned
                ).first()

                if conflicting:
                    return ApiResponse(
                        f"Employee (id={employee_id}) already has a scheduled visit at {datetime_planned}.",
                        False
                    ).return_response(), 400

        calendar_data = {
            "datetime_created": data.get("datetime_created", datetime.utcnow()),
            "datetime_planned": data.get("datetime_planned", datetime.utcnow())
        }
        calendar = Calendar(**calendar_data)
        calendar_repo = CalenderRepository(session)
        calendar_repo.create(calendar)
        session.flush()


        visit_data = {
            "name": data.get("name", ''),
            "description": data.get("description"),
            "calendar_id": calendar.id
        }
        visit = Visit(**visit_data)
        visit_repo = VisitRepository(session)
        visit_repo.create(visit)
        session.flush()

        employee_id = data.get("employee_id")
        visit_employee = None
        if employee_id:
            visit_employee = VisitEmployee(visit_id=visit.id, employee_id=employee_id)
            visit_employee_repo = VisitEmployeeRepository(session)
            visit_employee_repo.create(visit_employee)

        animal_id = data.get("animal_id")
        visit_animal = None
        if animal_id:
            visit_animal = VisitAnimal(visit_id=visit.id, animal_id=animal_id)
            visit_animal_repo = VisitAnimalRepository(session)
            visit_animal_repo.create(visit_animal)

        session.commit()

        response_data = {
            "calendar": calendar.to_dict(),
            "visit": visit.to_dict(),
            "visit_employee": visit_employee.to_dict() if visit_employee else None
        }

        return ApiResponse(response_data, True).return_response(),200

    except Exception as e:
        session.rollback()
        return ApiResponse(f"Error creating visit: {str(e)}",False).return_response(), 400





@visit_bp.route('/edit/<int:visit_id>', methods=['PUT'])
def edit(visit_id):
    db = SessionLocal()

    try:
        data = request.get_json()

        visit = db.query(Visit).filter_by(id=visit_id).first()
        if not visit:
            return ApiResponse(f"Visit with ID {visit_id} does not exist.", False).return_response(), 404

        calendar = db.query(Calendar).filter_by(id=visit.calendar_id).first()
        if not calendar:
            return ApiResponse("Associated calendar not found.", False).return_response(), 404

        visit.name = data.get("name", visit.name)
        visit.description = data.get("description", visit.description)

        new_datetime = data.get("datetime_planned")
        if new_datetime:
            if isinstance(new_datetime, str):
                new_datetime = datetime.fromisoformat(new_datetime)

            employee_id = data.get("employee_id")
            if employee_id:
                existing_visit_ids = db.query(VisitEmployee.visit_id).filter_by(employee_id=employee_id).all()
                visit_ids = [v[0] for v in existing_visit_ids]

                if visit_ids:
                    conflicting = db.query(Visit).join(Calendar).filter(
                        Visit.id.in_(visit_ids),
                        Calendar.datetime_planned == new_datetime,
                        Visit.id != visit.id
                    ).first()

                    if conflicting:
                        return ApiResponse(
                            f"Pracownik (id={employee_id}) ma już wizytę na {new_datetime}.",
                            False
                        ).return_response(), 400

            calendar.datetime_planned = new_datetime

        if "employee_id" in data:
            employee_id = data["employee_id"]
            visit_employee = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()

            if visit_employee:
                visit_employee.employee_id = employee_id
            else:
                visit_employee = VisitEmployee(visit_id=visit.id, employee_id=employee_id)
                visit_employee_repo = VisitEmployeeRepository(db)
                visit_employee_repo.create(visit_employee)

        if "animal_id" in data:
            animal_id = data["animal_id"]
            visit_animal = db.query(VisitAnimal).filter_by(visit_id=visit.id).first()

            if visit_animal:
                visit_animal.animal_id = animal_id
            else:
                visit_animal = VisitAnimal(visit_id=visit.id, animal_id=animal_id)
                visit_animal_repo = VisitAnimalRepository(db)
                visit_animal_repo.create(visit_animal)

        db.commit()

        visit_employee = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()
        visit_animal = db.query(VisitAnimal).filter_by(visit_id=visit.id).first()

        response = {
            "visit": visit.to_dict(),
            "calendar": calendar.to_dict(),
            "employee_id": visit_employee.employee_id if visit_employee else None,
            "animal_id": visit_animal.animal_id if visit_animal else None
        }

        return ApiResponse(response, True).return_response(), 200

    except Exception as e:
        db.rollback()
        return ApiResponse(f"Error editing the visit: {str(e)}", False).return_response(), 400



@visit_bp.route('/delete/<int:calender_id>', methods=['DELETE'])
def delete(calender_id):
    db = SessionLocal()

    try:
        repo = CalenderRepository(db)
        vist_repo = VisitRepository(db)
        visit_emp_rep = VisitEmployeeRepository(db)
        vist_animal_rep = VisitAnimalRepository(db)

        calendar = db.query(Calendar).filter_by(id=calender_id).first()
        if not calendar:
            return ApiResponse(f"Calendar with ID {calender_id} does not exist.", False).return_response(), 404


        visit = db.query(Visit).filter_by(calendar_id=calendar.id).first()
        if not visit:
            return ApiResponse(f"No visit associated with calendar ID {calender_id}.", False).return_response(), 404


        visit_emp = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()

        visit_animal = db.query(VisitAnimal).filter_by(visit_id=visit.id).first()

        if visit_animal:
            vist_animal_rep.delete(visit_animal)

        if visit_emp:
            visit_emp_rep.delete(visit_emp)

        vist_repo.delete(visit)
        repo.delete(calendar)

        return ApiResponse("The visit and related data have been marked as deleted.", True).return_response(), 200


    except Exception as e:
        db.rollback()
        return ApiResponse(f"Error deleting the visit: {str(e)}", False).return_response(), 400






@visit_bp.route('/list', methods=['GET'])
def list():
    db = SessionLocal()

    try:
        visit_repo = VisitRepository(db)
        visits = db.query(Visit).all()

        result = []

        for visit in visits:
            calendar = db.query(Calendar).filter_by(id=visit.calendar_id).first()
            visit_employee = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()

            result.append({
                "visit": visit.to_dict(),
                "calendar": calendar.to_dict() if calendar else None,
                "employee_id": visit_employee.employee_id if visit_employee else None
            })

        return ApiResponse(result, True).return_response(), 200

    except Exception as e:
        return ApiResponse(f"Error fetching visits: {str(e)}", False).return_response(), 400



@visit_bp.route('/view/<int:visit_id>', methods=['GET'])
def get_visit(visit_id):
    db = SessionLocal()

    try:
        visit = db.query(Visit).filter_by(id=visit_id).first()
        if not visit:
            return ApiResponse(f"Visit with ID {visit_id} does not exist.", False).return_response(), 404


        calendar = db.query(Calendar).filter_by(id=visit.calendar_id).first()

        visit_employee = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()

        result = {
            "visit": visit.to_dict(),
            "calendar": calendar.to_dict() if calendar else None,
            "employee_id": visit_employee.employee_id if visit_employee else None
        }


        return ApiResponse(result, True).return_response(), 200

    except Exception as e:
        return ApiResponse(f"Error fetching visit: {str(e)}", False).return_response(), 400

