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
                        f"Pracownik (id={employee_id}) ma już zaplanowaną wizytę na {datetime_planned}.",
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

    finally:
        session.close()



@visit_bp.route('/edit', methods=['POST'])
def edit():
    """
        Expect form content
        Return 200 or 400
        """
    return ApiResponse('OK', True, {}).return_response(), 201


@visit_bp.route('/delete', methods=['DELETE'])
def delete():
    """
        Expect visit identifier
        Return 200 or 400
        """
    return ApiResponse('OK', True, {}).return_response(), 201


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

    finally:
        db.close()

@visit_bp.route('/view/<int:visit_id>', methods=['GET'])
def get_visit(visit_id):
    db = SessionLocal()

    try:
        visit = db.query(Visit).filter_by(id=visit_id).first()
        if not visit:
            return ApiResponse(f"Wizyta o ID {visit_id} nie istnieje.", False).return_response(), 404

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

    finally:
        db.close()