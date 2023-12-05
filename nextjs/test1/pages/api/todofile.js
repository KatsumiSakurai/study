import { NextApiRequest, NextApiResponse } from "next";

const todofile = async (request, response) => {
    try {
        const fs = require('fs');
        const { method } = request;
        switch (method) {
            case "GET":
                console.log("GET")
                fs.readFile("todo.json", "utf-8", (err, data) => {
                    if (err) throw err;
                    console.log(data);
                    data = JSON.parse(data);
                    console.log(data);
                    response.status(200).json(data);
                });
                break;
            case "POST":
                console.log(request.body);
                console.log("xx1"); 
                var data = JSON.stringify(request.body);
                console.log(data);
                fs.writeFile("todo.json", data, (err) => {
                    if (err) throw err;
                    console.log("todoをファイルにほぞんしました");
                });
                console.log("xx2"); 
                response.status(200);
                break;
        }
    } catch (err) {
        response.status(500).json({ statusCode: 500, message: err.message });
    }
};

export default todofile;