from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # Ubah URL sesuai kebutuhan
db = SQLAlchemy(app)


class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    nama_depan = db.Column(db.String(50), nullable=False)
    nama_belakang = db.Column(db.String(50), nullable=False)


class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    jabatan = db.Column(db.String(50), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'), nullable=False)


db.create_all()


@app.route('/tambah_data', methods=['POST'])
def tambah_data():
    data = request.get_json()

    new_person = Person(nama_depan=data['nama_depan'], nama_belakang=data['nama_belakang'])
    db.session.add(new_person)
    db.session.commit()

    new_employee = Employee(jabatan=data['jabatan'], person_id=new_person.person_id)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'message': 'Data berhasil ditambahkan!'})


@app.route('/ambil_data', methods=['GET'])
def ambil_data():
    employees = Employee.query.join(Person).all()

    data_list = []
    for employee in employees:
        data_list.append({
            'person_id': employee.person_id,
            'nama_depan': employee.nama_depan,
            'nama_belakang': employee.nama_belakang,
            'jabatan': employee.jabatan
        })

    return jsonify({'data': data_list})


@app.route('/hapus_data/<int:person_id>', methods=['DELETE'])
def hapus_data(person_id):
    person = Person.query.get(person_id)

    if not person:
        return jsonify({'message': 'Person tidak ditemukan!'})

    db.session.delete(person)
    db.session.commit()

    return jsonify({'message': 'Data berhasil dihapus!'})

if __name__ == '__main__':
    app.run(debug=True)
