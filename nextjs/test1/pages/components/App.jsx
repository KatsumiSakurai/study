import React, { Component } from 'react';
import Form from './Form';
import List from  './List';
import Edit from  './Edit';

export default class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      todo: [],
      showEdit: false,
      editIndex: 0,
    };
    this.file = null;
    this.handleAdd = this.handleAdd.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.handleSaveData = this.handleSaveData.bind(this);
    this.handleLoadData = this.handleLoadData.bind(this);
  }

  componentDidMount() {
    this.handleLoadData();
  }

  // データ保存
  handleAdd(e){
    console.log(e);
    e.preventDefault();
    // フォームから受け取ったデータをオブジェクトに挿入して、stateのtodo配列に追加
    this.state.todo.push({title: e.target.title.value, date: e.target.date.value});
    // setStateを使ってstateを上書き
    this.setState({todo: this.state.todo});
    // inputのvalueを空に
    e.target.title.value = '';
    this.handleSaveData();
  }

  // データ削除
  handleRemove(i){
    // todo配列からi番目から1つ目のデータを除外
    this.state.todo.splice(i,1);
    // setStateでtodo配列を上書き
    this.setState({todo: this.state.todo});
    this.handleSaveData();
  }

  handleEdit(i) {
    // console.log(this.state.todo[i]['title']);
    this.setState({showEdit: true});
    this.setState({editIndex: i});

  }

  handleSave(e) {
    e.preventDefault();
    console.log(e.target.title.value);
    var todos = this.state.todo;
    // フォームから受け取ったデータをオブジェクトに挿入して、stateのtodo配列に追加
    todos[this.state.editIndex] = {title: e.target.title.value, date: e.target.date.value};
    // setStateを使ってstateを上書き
    this.setState({todo: todos});
    // inputのvalueを空に
    e.target.title.value = '';
    this.setState({showEdit: false});
    this.handleSaveData();
  }

  handleSaveData() {
    fetch("/api/todofile", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.state.todo)
    }).then((data) => {
      console.log(data);
    }).catch(error => {
      console.log(error);
    })
  }

  handleLoadData() {
    fetch("/api/todofile")
    .then(result => result.json())
    .then(data => {
      console.log(data);
      this.setState({todo: data});
    }).catch(error => {
      console.log(error);
    })
  }

  render() {
    return (
      <div className="siimple-box siimple--bg-dark">
        <h1 className="siimple-box-title siimple--color-white">React Todo App</h1>
        <Form handleAdd={this.handleAdd}/>
        <div className="siimple-rule"></div>
        <List todos={this.state.todo} handleRemove={this.handleRemove} handleEdit={this.handleEdit} />
        { this.state.showEdit
          ? <Edit
            handleSave={this.handleSave}
            todo={this.state.todo[this.state.editIndex]['title']}
            date={this.state.todo[this.state.editIndex]['date']}
            />
          : null }
      </div>
    );
 }
}