module example.com/hello

go 1.17

replace example.com/greetings => ../2-create-module

require example.com/greetings v0.0.0-00010101000000-000000000000
