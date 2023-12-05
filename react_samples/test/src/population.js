import React, { Component } from 'react'
import ReactFlexyTable from 'react-flexy-table'
import 'react-flexy-table/dist/index.css'
import ReactLoading from 'react-loading'
import Detail from './detail'

export default class population extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: false,
            hasError: false,
            name: '',
            detail: ''
        }
    }

    get_detail(name) {
        // this.fecthData('https://vw9d3y3k55.execute-api.ap-northeast-1.amazonaws.com/test2/detail?name=' + name);
        this.fecthData('https://d3anifybrnto0.cloudfront.net/test2/detail?name=' + name);
    }

    fecthData(url) {
        this.setState({ isLoading: true});
        fetch(url, {
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        })
        .then((response) => {
            this.setState({ isLoading: false });
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            this.setState({ detail: data });
        })
        .catch(() => this.setState({ hasError: true }));
    }

    render() {
        if (this.props.isLoading) {
            return <div><ReactLoading type="spin" color="#111"/></div>
        }
        if (this.props.hasError) {
            return <h2>error</h2>
        }
        const additionalCols = [
            {
                header: 'Action',
                td: (data) => {
                    return (
                        <div>
                            <button onClick={() => {
                                this.setState({name: data['地域名']});
                                this.get_detail(data['地域名']);
                            }}>詳細</button>
                        </div>
                    )
                }
            }
        ]
        if (this.state.name !== '') {
            return (
                <div>
                    <div id="overlay">
                        <div id="content">
                            <Detail 
                                isLoading={this.state.isLoading}        
                                hasError={this.state.hasError}
                                detail={this.state.detail}
                                 />
                            <button onClick={() => this.setState({name: ''})}>閉じる</button>
                        </div>
                    </div>
                </div>
            );
        }
        return (
            <div>
                <ReactFlexyTable data={this.props.data} sortable pageSize="20" additionalCols={additionalCols}/>
            </div>
        );
    }
}