#database initialization for instance tracking -------------------------------------
# conn = sql.connect("db.db")
# curse = conn.cursor()
#
# curse.execute(
#     """
#     CREATE TABLE IF NOT EXISTS Envs(
# 	envID INTEGER NOT NULL AUTOINCREMENT,
# 	domainName VARCHAR(20) UNIQUE NOT NULL,
# 	agentIndex INTEGER NOT NULL,
# 	agentAPIKey VARCHAR(12) NOT NULL,
# 	PRIMARY KEY (envID, domainName, agentIndex)
#     );
#     """
# )
# conn.commit()
# curse.close()
# conn.close()
#--------------------------------------------------------------------------------------
#DEPRECATED

#
# def connector()->[sql.Connection,sql.Cursor]:
#     """
#     simplification of cursor creations
#
#     :return: sqlite3 connector, cursor
#     """
#     conn=sql.connect("db.db")
#     curse = conn.cursor()
#     return conn, curse