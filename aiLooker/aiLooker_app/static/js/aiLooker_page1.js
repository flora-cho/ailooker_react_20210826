'use strict';
const e = React.createElement;

function App() {
  const [list             , setList            ] = React.useState([]);
  const [count            , setCount           ] = React.useState(0);
  const [pages            , setPages           ] = React.useState([]);
  const [page             , setPage            ] = React.useState(0);
  const [showModal        , setShowModal       ] = React.useState(false);
  const [modalDescription , setModalDescription] = React.useState("");
  const [itemId           , setItemId          ] = React.useState(null);
  const [error            , setError           ] = React.useState("");
  const [file             , setFile            ] = React.useState(null);

  // 광고 신규등록을 위한 변수 초기화
  const advtInitialState = {
    advtno: 0,
    advttpcd: '',
    advttitl: '',
    advtstadate: '',
    advtenddate: '',
    advtdesc: '',
    advtgrdcd: '',
    filepath: '',
    delyn: 'N',
    fstaddtmst: '',
    fstaddid: '',
    lastupttmst: '',
    lastuptid: '',
  };

  // 광고 검색 조건을 위한 변수 초기화
  const searchInitialState = {
    advttitl: '',
    delyn: '',
    advtstadate: '',
    advtenddate: '',
    advtgrdcd: '',
    advttpcd: '',
  }

  const [advt, setAdvt] = React.useState(advtInitialState);
  const [search, setSearch] = React.useState(searchInitialState);

  // 광고 등록 화면 input 값 입력 시 호출 되는 함수 (+버튼 클릭 시)
  const changeAdvt = (e) => {
    const { name, value } = e.target;

    setAdvt({
      ...advt,
      [name]: value,
    })
  }

  // 광고 검색 조건 input 값 입력 시 호출 되는 함수
  const changeSearch = (e) => {
    const { name, value } = e.target;

    setSearch({
      ...search,
      [name]: value,
    })
  }

  // 파일 첨부시 호출 되는 함수
  const changeFile = (e) => {
    // 아래의 2가지 방법 중에 API랑 더 잘맞는거 쓰시면 됩니다.

    // 파일 객체 자체를 저장
    setFile(e.target.files[0]);

    // 파일을 url로 수정해 저장
    setAdvt({
      ...advt,
      filepath: window.URL.createObjectURL(e.target.files[0])
    })
  }

  const success = (data) => {
    setList(data.data);
    setCount(data.count);

    const newPages = [];

    if (data.count > 5) {
      for (let i=0; i<Math.ceil(data.count / 5); i++) {
        newPages.push({
          name: (i+1).toString(),
          page: i,
        });
        console.log("page",i);
      }

      if (page > newPages.length-1) {
        setPage(page-1);
      }
      
    } else {
      setPage(0);
    }
    setPages(newPages);
  };

  const logout = async ()=>{
    await localStorage.setItem("aiLookerToken",null);
    window.location = "/login";
  };

  const getData = ()=>{
    get_aiLookers_api(page, success, (text) => { console.log("Error: ", text) });
  };

  // 광고 신규등록 버튼 클릭시 호출 되는 함수
  const newTbladvtbsc = ()=>{
    setModalDescription("광고 신규등록");

    // 신규 등록 input값 초기 과정 (입력 하고 닫고 다시 열었을 경우)
    setAdvt(advtInitialState);
    setError("");
    setFile(null);

    // 팝업창 호출 함수
    setShowModal(true);

    const itemInput = document.getElementById("itemInput");
    setTimeout(() => { itemInput && itemInput.focus() }, 1);
  };

  // 광고 수정 버튼 클릭 시 호출 되는 함수
  const editTbladvtbsc = (data)=>{
    setModalDescription("광고 관리 상세");

    // 수정 하려는 광고 data input value에 담아주기
    setAdvt({
      advtno: data.advtno,
      advttpcd: data.advttpcd,
      advttitl: data.advttitl,
      advtstadate: data.advtstadate,
      advtenddate: data.advtenddate,
      advtdesc: data.advtdesc,
      advtgrdcd: data.advtgrdcd,
      filepath: data.filepath,
      delyn: data.delyn,
      fstaddtmst: data.fstaddtmst,
      fstaddid: data.fstaddid,
      lastupttmst: data.lastupttmst,
      lastuptid: data.lastuptid,
    });
    setError("");

    // 팝업창 호출 함수
    setShowModal(true);
    const itemInput = document.getElementById("itemInput");
    setTimeout(() => { itemInput && itemInput.focus() }, 1);
  };

  // 광고 저장 함수
  const saveTbladvtbsc = (e)=>{
    e.preventDefault();
    setError("");

    // print
    console.log("saving new", advt);

    // 저장 API 호출 조건
    if (advt.advtno.length === 0)
      setError("Please enter advtno");
    else {
      if (advt.advtno === null)
        post_aiLooker_api({
          advttpcd: advt.advttpcd, 
          advttitl: advt.advttitl, 
          advtstadate: advt.advtstadate, 
          advtenddate: advt.advtenddate, 
          advtdesc: advt.advtdesc, 
          advtgrdcd: advt.advtgrdcd
        }, () => { getData(); });
      else
        put_aiLooker_api(advt.advtno, {
          advttpcd: advt.advttpcd, 
          advttitl: advt.advttitl, 
          advtstadate: advt.advtstadate, 
          advtenddate: advt.advtenddate, 
          advtdesc: advt.advtdesc, 
          advtgrdcd: advt.advtgrdcd
        }, () => { getData(); });
      setShowModal(false);
    }
  };

  // 광고 삭제 함수
  const deleteTbladvtbsc = (advtno) => {
    // print
    console.log("delete advt", advtno);
    
    // 삭제 여부 확인 창
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      // 삭제 실행
      if (result.isConfirmed) {
        delete_aiLooker_api(advtno, ()=>{
          Swal.fire({
              title: 'Deleted!',
              text: "Your advtno has been deleted!",
              icon: 'success',
              timer: 1000,
          });
          getData();
        });
        // 광고 관리 상세 창 닫기
        setShowModal(false);
      }
    });
  };

  const keyDownHandler = (e)=>{
    if (e.which === 27)
      setShowModal(false);
  };

  // 첫 화면 렌더시 데이터 요청 함수 진행
  React.useEffect(()=>{
    getData();
  }, [page]);

  return (
    <div onKeyDown={keyDownHandler}>
      {/* 광고 등록 및 수정 팝업창 */}
      <div style={{background: "#00000060"}}
          className={"modal " + (showModal?" show d-block":" d-none")} tabIndex="-1" role="dialog">
        <div className="modal-dialog shadow">
          <form method="post">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{modalDescription}</h5>
              <button type="button" className="btn-close" onClick={()=>{setShowModal(false)}} aria-label="Close"></button>
            </div>
            <div className="modal-body">
              <label>광고번호</label>
                <div className="form-group">
                  {/* name, value가 가르키는 변수가 동일해야 정상작동 됨 */}
                  <input type="text" className="form-control" name="advtno" id="itemInput"
                         value={advt.advtno} onChange={changeAdvt}
                         placeholder="광고번호"/>     
                </div>
              <label style={{marginTop: "1em"}}>광고유형</label>
                <div className="form-group" >
                  <input type="text" className="form-control" placeholder="광고유형"
                         value={advt.advttpcd} onChange={changeAdvt}
                         name="advttpcd" />
                </div>
              <label style={{marginTop: "1em"}}>광고제목</label>
                <div className="form-group">
                  <input type="text" className="form-control"
                         value={advt.advttitl} onChange={changeAdvt}
                         placeholder="광고제목" name="advttitl" />
                </div>
                <label style={{marginTop: "1em"}}>광고시작일자</label>
                <div className="form-group">
                  <input type="text" className="form-control"
                         value={advt.advtstadate} onChange={changeAdvt}
                         placeholder="광고시작일자" name="advtstadate" />
                </div>
                <label style={{marginTop: "1em"}}>광고종료일자</label>
                <div className="form-group">
                  <input type="text" className="form-control"
                         value={advt.advtenddate} onChange={changeAdvt}
                         placeholder="광고종료일자" name="advtenddate" />
                </div>
                <div>
                  <label style={{marginTop: "1em"}}>파일 등록</label>
                  <div className="form-group">
                    <input type="file" className="form-control" onChange={changeFile} />
                  </div>
                </div>
                {/* 등록  */}
                { modalDescription === '광고 관리 상세' && 
                  <div>
                    <label style={{marginTop: "1em"}}>기존 파일</label>
                    <a src={advt.filepath}></a>
                  </div>
                }
                <label style={{marginTop: "1em"}}>광고내용</label>
                <div className="form-group">
                  <input type="text" className="form-control"
                         value={advt.advtdesc} onChange={changeAdvt}
                         placeholder="광고내용" name="advtdesc" />
                </div>
                <label style={{marginTop: "1em"}}>광고등급</label>
                <div className="form-group">
                  <input type="text" className="form-control"
                         value={advt.advtgrdcd} onChange={changeAdvt}
                         placeholder="광고등급" name="advtgrdcd" />
                </div>
              <small className="form-text text-muted">{error}</small>
            </div>
            <div className="modal-footer">
              <a className="btn btn-light" style={{background: "white"}}
                onClick={saveTbladvtbsc}>
                <img style={{width: "40px", heigth: "40px", background: "white"}} src="/static/image/img3.png" alt="저장"/>
              </a>
              {/* 삭제 버튼은 신규 등록시 불필요하므로 수정 팝업창에서만 뜨는 조건 */}
              { modalDescription === '광고 관리 상세' && 
                <a className="btn btn-light" style={{background: "white"}}
                  onClick={()=>{deleteTbladvtbsc(advt.advtno)}}>
                  <img style={{width: "40px", heigth: "40px"}} src="/static/image/img1.jpg" alt="삭제"/>
                </a>
              }
            </div>
          </div>
          </form>
        </div>
      </div>

      {/* 광고 메인 화면 */}
      <div style={{maxWidth: "1000px", margin: "auto", marginTop: "1em", marginBottom: "1em",
                    padding: "1em"}} className="shadow">
        {/* <div style={{display: "flex", flexDirection: "row"}}>
          <span>[0010-광고관리]</span>
          <a className="btn btn-light" style={{marginLeft: "auto"}} onClick={logout}>Logout</a>
        </div> */}
        <div style={{display: "flex", flexDirection: "row"}}>
          {/* table로 title, logout, search box를 묶어서 생성함 */}
          <table style={{width: "100%" }}>
            <thead>
              <tr>
                <th colSpan="3">[0010-광고관리]</th>
                <th>
                <a className="btn btn-light" style={{marginLeft: "auto"}} onClick={logout}>Logout</a>
                </th>
              </tr> 
            </thead>
            <tbody>
              <tr>
                <td>광고제목</td>
                <td>
                  <input type="text" className="form-control" name="advttitl"
                    value={search.advttitl} onChange={changeSearch}
                    placeholder="광고제목"/>
                </td>
                <td>삭제여부</td>
                <td>
                  <input type="text" className="form-control" name="delyn"
                    value={search.delyn} onChange={changeSearch}
                    placeholder="All"/>
                </td>
              </tr>
              <tr>
                <td>시작일자</td>
                <td>
                  <input type="text" className="form-control" name="advtstadate"
                    value={search.advtstadate} onChange={changeSearch}
                    placeholder="YYYYMMDD"/>
                </td>
                <td>종료일자</td>
                <td>
                  <input type="text" className="form-control" name="advtenddate"
                    value={search.advtenddate} onChange={changeSearch}
                    placeholder="YYYYMMDD"/>
                </td>
              </tr>
              <tr>
                <td>광고유형</td>
                <td>
                  <input type="text" className="form-control" name="advtgrdcd"
                    value={search.advtgrdcd} onChange={changeSearch}
                    placeholder="광고유형"/>
                </td>
                <td>광고등급</td>
                <td>
                  <input type="text" className="form-control" name="advttpcd"
                    value={search.advttpcd} onChange={changeSearch}
                    placeholder="광고등급"/>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      {/* DB에 저장되어있는 광고 리스트 */}
      <div style={{maxWidth: "1000px", margin: "auto", marginTop: "1em", marginBottom: "1em",
                    padding: "1em"}} className="shadow">
        <div style={{display: "flex", flexDirection: "row", marginBottom: "5px"}}>
          {pages.length > 0 && <nav className="d-lg-flex justify-content-lg-end dataTables_paginate paging_simple_numbers">
            <ul className="pagination">
              <li className={"page-item " + (page === 0?"disabled":"")} onClick={(e)=>{
                    e.preventDefault();
                    setPage(Math.max(page-1,0));
              }}><a className="page-link" href="#" aria-label="Previous"><span
                  aria-hidden="true">«</span></a></li>
              {pages.map((el)=><li key={"page" + el.page} onClick={(e)=>{
                  setPage(el.page);
                }} className={"page-item "+(page===el.page?"active":"")}>
                <a className="page-link" href="#">
                  {el.name}
                </a></li>)}
              <li className={"page-item " + (page === pages.length-1?"disabled":"")} onClick={()=>{
                    setPage(Math.min(page+1,pages.length-1));
              }}><a className="page-link" href="#" aria-label="Next"><span
                  aria-hidden="true">»</span></a></li>
            </ul>
          </nav>}
          <a className="btn btn-light" style={{marginLeft: "auto", background: "white"}}
             onClick={newTbladvtbsc}
          >
            <img style={{width: "40px", heigth: "40px"}} src="/static/image/img4.png" alt="신규 광고 등록"/>
          </a>
        </div>
        <table className="table table-hover caption-top">
          <thead className="table-light">
            {/* table의 head setting */}
          <tr>
            <th></th>
            <th>광고번호</th>
            <th>광고종류</th>
            <th>광고제목</th>
            <th>광고시작일자</th>
            <th>광고종료일자</th>
            <th>광고내용</th>
            <th>광고등급</th>
            <th>삭제여부</th>
          </tr>
          </thead>
          <tbody>
            {/* table의 body */}
            {/* list 배열을 map 함수를 통해 반복문을 돌면서 화면에 출력 */}
          { list.map((row) =>
            <tr key={row.advtno}>
              <td>
                {/* row 별 광고 수정 버튼 */}
                <a className="btn btn-light" style={{marginLeft: "auto", background: "white"}}
                  onClick={()=>{editTbladvtbsc(row)}}>
                    <img style={{width: "40px", heigth: "40px"}} src="/static/image/img2.png" alt="수정"/>
                  </a>
              </td>
              <td>{row.advtno}</td>
              <td>{row.advttpcd}</td>
              <td>{row.advttitl}</td>
              <td>{row.advtstadate}</td>
              <td>{row.advtenddate}</td>
              <td>{row.advtdesc}</td>
              <td>{row.advtgrdcd}</td>
              <td>{row.delyn}</td>
            </tr>
          )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// reactAppContainer라는 id를 가진 요소를 찾아서 구현한 함수를 렌더하겠다.
const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
  e(App),
  domContainer
);
