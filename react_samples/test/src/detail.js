import React, { Component } from 'react'
import ReactFlexyTable from 'react-flexy-table'
import 'react-flexy-table/dist/index.css'
import ReactLoading from 'react-loading'

export default class Detail extends Component {
    constructor(props) {
        super(props);
        this.state = {
        }
    }

    render() {
        if (this.props.isLoading) {
            return <div><ReactLoading type="spin" color="#111"/></div>
        }
        if (this.props.hasError) {
            return <h2>error</h2>
        }
        if (this.props.detail === '') {
            return <h2>building</h2>
        }
        return (
            <div>
                <ReactFlexyTable data={this.props.detail} sortable pageSize={20} />
            </div>
        );
    }
}