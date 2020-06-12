from pydrill.client import PyDrill

# or use PYDRILL_HOST PYDRILL_PORT
conn = PyDrill(host='localhost', port=8047)

assert conn.is_active()

employees = conn.query('''
  SELECT * FROM cp.`employee.json` LIMIT 5
''')
