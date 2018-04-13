$dataSource = "SQLServer Instance Name"
$database = "Database Name"
$connectionString = "Server=$dataSource;Database=$database;IntegratedSecurity=True;"

$query = Select column from table where column = 'value'

$connection = "New-Object System.Data.SqlClient.SqlConnection"
$connection.ConnectionString = $connectionString
$connection.Open()
$command = $connection.CreateCommand()
$command.CommandText = $query

$result = $command.ExecuteScalar()

$connection.Close()
