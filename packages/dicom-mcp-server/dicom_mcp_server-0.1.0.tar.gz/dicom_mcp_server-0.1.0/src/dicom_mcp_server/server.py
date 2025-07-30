from mcp.server.fastmcp import FastMCP
import requests
import os
import pydicom
from pydicom.errors import InvalidDicomError
from pynetdicom import AE, debug_logger
from pynetdicom.presentation import PresentationContext
from pynetdicom.presentation import build_context
from typing import List, Dict
from pydicom.uid import UID
from pydicom.tag import Tag
from pydicom.datadict import dictionary_description, dictionary_keyword, dictionary_VR, dictionary_VM

# Create an MCP server
mcp = FastMCP("dicom_mcp_server")

### Tool 1 : Dicom 파일을 읽고 parsing하여 정보를 표시합니다
@mcp.tool()
def read_dicom(file_path: str) -> str:
    """
    단일 DICOM 파일의 메타데이터 정보를 읽어 문자열로 반환합니다.

    주요 DICOM 태그(환자 정보, 검사 정보, UID 등)를 추출하여 사람이 읽기 쉬운 형태로 
    요약합니다. 파일이 없거나 유효한 DICOM 형식이 아니면 오류 메시지를 반환합니다.

    Args:
        file_path (str): 읽어올 DICOM 파일의 전체 경로입니다.

    Returns:
        str: DICOM 메타데이터 정보를 담은 문자열 또는 오류 발생 시 오류 메시지입니다.
    """
    try:
        dataset = pydicom.dcmread(file_path)
    
        info = []
        info.append(f"환자 이름: {dataset.get('PatientName', '정보 없음')}")
        info.append(f"환자 ID: {dataset.get('PatientID', '정보 없음')}")
        info.append(f"Study 유형 (Modality): {dataset.get('Modality', '정보 없음')}")
        info.append(f"Study 설명: {dataset.get('StudyDescription', '정보 없음')}")
        info.append(f"시리즈 설명: {dataset.get('SeriesDescription', '정보 없음')}")
        info.append(f"Study UID (Study Instance UID): {dataset.get('StudyInstanceUID', '정보 없음')}")
        info.append(f"시리즈 UID (Series Instance UID): {dataset.get('SeriesInstanceUID', '정보 없음')}")
        info.append(f"Sop UID (SOP Instance UID): {dataset.get('SOPInstanceUID', '정보 없음')}")
        info.append(f"전송 구문 (Transfer Syntax): {dataset.file_meta.TransferSyntaxUID.name if dataset.file_meta and hasattr(dataset.file_meta, 'TransferSyntaxUID') and dataset.file_meta.TransferSyntaxUID else '정보 없음'}")
        return "\n".join(info) 
        
    except InvalidDicomError:
        print(f"오류: {file_path} 은(는) 유효한 DICOM 파일이 아닙니다.")
        return "DICOM 파일 읽기 실패"
    except FileNotFoundError:
        print(f"오류: {file_path} 에서 파일을 찾을 수 없습니다.")
        return "DICOM 파일 읽기 실패"


### Tool 2: 특정 경로하에 있는 Dicom 파일을 모두 읽고, study-series-instance 단위로 분류하여 각각의 정보를 표시합니다
@mcp.tool()
def read_dicom_files(directory_path: str) -> str:
    """
    지정된 디렉토리 (및 하위 디렉토리) 내의 모든 DICOM 파일들을 읽고 요약 정보를 반환합니다.

    파일들을 스캔하여 공통적인 검사 정보(환자 정보, 검사 설명, 검사 UID 등)와 
    각 시리즈별 정보(시리즈 UID, Modality, 시리즈 설명, 인스턴스 수)를 요약하여 
    문자열 형태로 제공합니다. DICOM 파일이 없거나 읽기 오류 발생 시 해당 정보를 포함합니다.

    Args:
        directory_path (str): DICOM 파일들을 검색할 디렉토리의 경로입니다. 
                             하위 디렉토리까지 모두 검색합니다.

    Returns:
        str: 디렉토리 내 DICOM 파일들의 요약 정보 또는 오류 메시지를 담은 문자열입니다.
    """
    dicom_file_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(".dcm"):
                dicom_file_paths.append(os.path.join(root, file))

    if not dicom_file_paths:
        return f"경로에서 DICOM 파일을 찾을 수 없습니다: {directory_path}"

    study_details = {}
    overall_transfer_syntax = "정보 없음"
    study_info_set = False
    # Key: SeriesInstanceUID, Value: Dict with Modality, SeriesDescription, InstanceCount
    series_data = {} 
    
    processed_files_count = 0
    errors_encountered = []

    for dcm_path in dicom_file_paths:
        try:
            # force=True can help with slightly non-compliant files
            dataset = pydicom.dcmread(dcm_path, force=True) 
            
            if not study_info_set:
                study_details['PatientName'] = dataset.get('PatientName', '정보 없음')
                study_details['PatientID'] = dataset.get('PatientID', '정보 없음')
                study_details['StudyDescription'] = dataset.get('StudyDescription', '정보 없음')
                study_details['StudyInstanceUID'] = dataset.get('StudyInstanceUID', '정보 없음')
                if dataset.file_meta and hasattr(dataset.file_meta, 'TransferSyntaxUID') and dataset.file_meta.TransferSyntaxUID:
                    overall_transfer_syntax = dataset.file_meta.TransferSyntaxUID.name
                else:
                    overall_transfer_syntax = "정보 없음 (파일 메타가 없거나 TransferSyntaxUID를 찾을 수 없음)"
                study_info_set = True

            # Use a placeholder if SeriesInstanceUID is missing to avoid losing track of the series
            series_uid = dataset.get('SeriesInstanceUID', f'미확인시리즈_{len(series_data)}')
            
            if series_uid not in series_data:
                series_data[series_uid] = {
                    'Modality': dataset.get('Modality', '정보 없음'),
                    'SeriesDescription': dataset.get('SeriesDescription', '정보 없음'),
                    'InstanceCount': 0
                }
            series_data[series_uid]['InstanceCount'] += 1
            processed_files_count +=1

        except InvalidDicomError:
            error_msg = f"잘못된 DICOM 파일: {dcm_path}"
            errors_encountered.append(error_msg)
            print(error_msg) 
        except Exception as e:
            error_msg = f"DICOM 파일 읽기 오류 {dcm_path}: {str(e)}"
            errors_encountered.append(error_msg)
            print(error_msg)

    if processed_files_count == 0: # No file could be successfully read
        error_summary = "\n  - ".join(errors_encountered)
        return f"'{directory_path}'에서 DICOM 파일을 성공적으로 읽을 수 없었습니다.\n발생한 오류:\n  - {error_summary if errors_encountered else '기록된 특정 오류는 없지만 추출된 데이터가 없습니다.'}"
    
    if not study_info_set : # Should ideally be caught by processed_files_count == 0
         return f"{processed_files_count}개의 파일을 처리했지만 '{directory_path}'에서 공통 검사 정보를 확인할 수 없었습니다."

    result_str_parts = [f"'{directory_path}' 내 DICOM 파일 요약:\n"]

    result_str_parts.append("검사 정보 (성공적으로 읽은 첫 번째 파일 기준):")
    result_str_parts.append(f"  환자 이름: {study_details.get('PatientName', '정보 없음')}")
    result_str_parts.append(f"  환자 ID: {study_details.get('PatientID', '정보 없음')}")
    result_str_parts.append(f"  Study 설명: {study_details.get('StudyDescription', '정보 없음')}")
    result_str_parts.append(f"  Study UID (Study Instance UID): {study_details.get('StudyInstanceUID', '정보 없음')}")
    result_str_parts.append(f"\n전체 전송 구문 (성공적으로 읽은 첫 번째 파일 기준): {overall_transfer_syntax}\n")

    if series_data:
        result_str_parts.append("시리즈 상세 정보:")
        series_counter = 0
        for uid, data in series_data.items():
            series_counter += 1
            result_str_parts.append(f"  --- 시리즈 {series_counter} ---")
            result_str_parts.append(f"  시리즈 UID (Series Instance UID): {uid}")
            result_str_parts.append(f"  Study 유형 (Modality): {data['Modality']}")
            result_str_parts.append(f"  시리즈 설명: {data['SeriesDescription']}")
            result_str_parts.append(f"  인스턴스 수: {data['InstanceCount']}")
    else:
        result_str_parts.append("시리즈 정보를 추출할 수 없었습니다 (일부 파일이 처리되었을 수 있음).")
        
    if errors_encountered:
        result_str_parts.append("\n일부 파일 처리 중 문제 발생:")
        for err in errors_encountered:
            result_str_parts.append(f"  - {err}")

    return "\n".join(result_str_parts)


### Tool 3 : 특정 storescu에게 명시된 dcm파일을 전송합니다.
@mcp.tool()
def send_dicom_to_scp(ae_title: str, ip_address: str, port: int, source_path: str) -> str:
    """
    지정된 DICOM 파일 또는 디렉토리 내의 모든 DICOM 파일들을 원격 Store SCP로 전송 (C-STORE SCU 역할).

    source_path가 단일 파일이면 해당 파일만, 디렉토리이면 해당 디렉토리 (및 하위 디렉토리) 내의 
    모든 .dcm 파일을 대상으로 합니다. 각 파일의 SOP Class UID와 Transfer Syntax UID를 읽어 
    적절한 Presentation Context를 구성하여 SCP와 협상 후 전송을 시도합니다.

    Args:
        ae_title (str): 대상 Store SCP의 AE Title입니다.
        ip_address (str): 대상 Store SCP의 IP 주소입니다.
        port (int): 대상 Store SCP의 포트 번호입니다.
        source_path (str): 전송할 단일 DICOM 파일의 경로 또는 DICOM 파일들이 포함된 
                         디렉토리의 경로입니다.

    Returns:
        str: 전송 시도 결과(성공/실패 요약, 각 파일별 상태, 오류 메시지 등)를 담은 문자열입니다.
    """

    dicom_files_to_send = []
    if not os.path.exists(source_path):
        return f"오류: 소스 경로 '{source_path}'를 찾을 수 없습니다."

    if os.path.isfile(source_path):
        if source_path.lower().endswith(".dcm"):
            dicom_files_to_send.append(source_path)
        else:
            return f"오류: '{source_path}'는 .dcm 파일이 아닙니다."
    elif os.path.isdir(source_path):
        for root, _, files in os.walk(source_path): # 재귀적 탐색
            for file_name in files:
                if file_name.lower().endswith(".dcm"):
                    dicom_files_to_send.append(os.path.join(root, file_name))
    else:
        return f"오류: '{source_path}'는 유효한 파일 또는 디렉토리가 아닙니다."

    if not dicom_files_to_send:
        return f"'{source_path}' 경로에서 전송할 DICOM 파일을 찾지 못했습니다."

    ae = AE()
    # 전송할 모든 dicom 파일에서 presentation, transfer syntax 조회해서 abstract_trasnfer_map에 추가
    abstract_trasnfer_map : Dict[str, List[str]] = dict()
    for i, filename in enumerate(dicom_files_to_send):
        curSlice = pydicom.read_file(filename, stop_before_pixels=True)
        sopClass = curSlice.file_meta.MediaStorageSOPClassUID
        transferSyntaxUid = curSlice.file_meta.TransferSyntaxUID
        abstract_trasnfer_map.setdefault(sopClass, []).append(transferSyntaxUid)

    # association 시 제안할 request_context 생성
    request_context_for_association : List[PresentationContext] = [build_context(sopClass) for sopClass in abstract_trasnfer_map.keys()]
    for idx, transferSyntaxUids in enumerate(abstract_trasnfer_map.values()):
        request_context_for_association[idx].transfer_syntax = transferSyntaxUids

    ae.requested_contexts = request_context_for_association
 
    assoc = ae.associate(ip_address, port, ae_title=ae_title)
    results = []

    if assoc.is_established:
        results.append(f"SCP '{ae_title}' ({ip_address}:{port})로 연결 성공.")
        successful_sends = 0
        failed_sends = 0

        for dcm_file_path in dicom_files_to_send:
            try:
                status = assoc.send_c_store(dcm_file_path) 
                file_basename = os.path.basename(dcm_file_path)
                if status and status.Status == 0x0000:
                    results.append(f"  성공: '{file_basename}' 전송 완료.")
                    successful_sends += 1
                else:
                    failed_sends += 1
                    if status:
                        results.append(f"  실패: '{file_basename}' 전송 실패. 상태: {hex(status.Status)} - {status.ErrorComment if hasattr(status, 'ErrorComment') else '세부 정보 없음'}")
                    else:
                        results.append(f"  실패: '{file_basename}' 전송 실패. SCP로부터 상태 응답 없음.")
            except Exception as e:
                failed_sends += 1
                results.append(f"  오류: '{os.path.basename(dcm_file_path)}' 처리 중 예외 발생 - {str(e)}")
        
        assoc.release()
        results.append(f"\n전송 요약: 총 {len(dicom_files_to_send)}개 파일 중 {successful_sends}개 성공, {failed_sends}개 실패.")
    else:
        results.append(f"SCP '{ae_title}' ({ip_address}:{port})로 연결 실패. 원인: {assoc.acceptor.primitive.result_str if assoc.acceptor and assoc.acceptor.primitive else '알 수 없음'}")

    return "\n".join(results)


### Tool 4: DICOM UID 문자열에 해당하는 이름을 반환합니다.
@mcp.tool()
def get_dicom_uid_name(uid_string: str) -> str:
    """
    입력받은 DICOM UID 문자열의 표준 이름을 반환합니다.

    SOP Class UID, Transfer Syntax UID, Meta SOP Class UID 등 다양한 UID의 
    사람이 읽기 쉬운 이름을 조회합니다. pydicom 라이브러리에 정의된 UID 정보를 사용합니다.

    Args:
        uid_string (str): 조회할 DICOM UID 문자열입니다. (예: "1.2.840.10008.5.1.4.1.1.2")

    Returns:
        str: 해당 UID의 이름 (예: "CT Image Storage"). 
             UID가 유효하지 않거나 pydicom 사전에 없는 경우 "알 수 없는 UID" 또는 
             오류 메시지를 반환할 수 있습니다.
    """
    try:
        uid_obj = UID(uid_string)
        if uid_obj.name and uid_obj.name != "Unknown":
            return uid_obj.name

    except ValueError: # UID 문자열 형식이 잘못된 경우
        return f"오류: 유효하지 않은 UID 형식입니다: {uid_string}"
    except Exception as e:
        return f"오류: UID 이름 조회 중 예외 발생 - {str(e)}"

### Tool 5: DICOM 태그 ID에 해당하는 정보를 반환합니다.
@mcp.tool()
def get_dicom_tag_info(tag_id_string: str) -> Dict[str, str]:
    """
    입력받은 DICOM 태그 ID 문자열에 해당하는 태그 정보(이름, 키워드, VR, VM)를 반환합니다.

    태그 ID는 "(gggg,eeee)", "gggg,eeee", "0xggggeeee" 형식 모두 지원합니다.
    pydicom 라이브러리에 내장된 DICOM 사전을 사용하여 정보를 조회합니다.

    Args:
        tag_id_string (str): 조회할 DICOM 태그 ID 문자열입니다. 
                             (예: "(0010,0010)", "0010,0010", "0x00100010")

    Returns:
        Dict[str, str]: 태그 정보를 담은 딕셔너리입니다. 
                        (예: {"tag_id": "(0010,0010)", "keyword": "PatientName", "name": "Patient's Name", "vr": "PN", "vm": "1"})
                        태그를 찾지 못하거나 오류 발생 시 오류 메시지를 포함한 딕셔너리를 반환합니다.
    """
    try:
        # 입력된 다양한 형식의 태그 문자열을 pydicom.tag.Tag 객체로 변환 시도
        if tag_id_string.startswith('0x') or tag_id_string.startswith('0X'):
            tag_val = int(tag_id_string, 16)
            tag_obj = Tag(tag_val)
        elif ',' in tag_id_string:
            parts = tag_id_string.replace('(', '').replace(')', '').split(',')
            if len(parts) == 2:
                group = int(parts[0].strip(), 16)
                element = int(parts[1].strip(), 16)
                tag_obj = Tag(group, element)
            else:
                raise ValueError("쉼표로 구분된 태그 형식 오류")
        else: # 단순 8자리 16진수 문자열로 가정 (예: "00100010")
             if len(tag_id_string) == 8:
                 tag_obj = Tag(int(tag_id_string[:4], 16), int(tag_id_string[4:], 16))
             else:
                 raise ValueError("8자리 16진수 태그 형식 오류")

        keyword = dictionary_keyword(tag_obj)
        name = dictionary_description(tag_obj)
        vr = dictionary_VR(tag_obj)
        vm = dictionary_VM(tag_obj)

        if name == "Unknown Tag": # pydicom에서 찾지 못한 경우
             return {"오류": f"알 수 없는 태그 ID 또는 정보 없음: {str(tag_obj)} ({tag_id_string})"} 

        return {
            "tag_id": str(tag_obj),
            "keyword": keyword if keyword else "정보 없음",
            "name": name,
            "vr": vr,
            "vm": vm
        }

    except ValueError as ve: # 태그 형식 변환 중 오류
        return {"오류": f"유효하지 않은 태그 ID 형식 또는 값입니다: {tag_id_string} - {str(ve)}"}
    except Exception as e:
        return {"오류": f"태그 정보 조회 중 예외 발생 - {str(e)}"}

def main():
    print("Starting DICOM MCP Server...")
    mcp.run()

if __name__ == "__main__":
    main()

